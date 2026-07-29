from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Student, AttendanceRecord, Course
from app.schemas.schemas import StudentAttendanceSummary, CourseAttendance, RiskAnalysisResponse, RiskStudent
from app.ml.attendance_model import train_attendance_model, predict_student_risk
from typing import List, Dict, Optional

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.get("/student/{student_id}", response_model=StudentAttendanceSummary)
def get_student_attendance(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found."
        )
        
    records = db.query(AttendanceRecord).filter(AttendanceRecord.student_id == student.id).all()
    
    if not records:
        return StudentAttendanceSummary(
            student_id=student.student_id,
            student_name=student.name,
            overall_percentage=0.0,
            courses=[]
        )
        
    # Group by course
    course_data: Dict[int, List[str]] = {}
    for r in records:
        if r.course_id not in course_data:
            course_data[r.course_id] = []
        course_data[r.course_id].append(r.status)
        
    courses_summary = []
    total_classes_all = 0
    total_present_all = 0
    
    for course_id, statuses in course_data.items():
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            continue
        total = len(statuses)
        present = sum(1 for s in statuses if s == "Present")
        pct = (present / total) * 100 if total > 0 else 0.0
        
        total_classes_all += total
        total_present_all += present
        
        courses_summary.append(CourseAttendance(
            course_code=course.course_id,
            course_name=course.course_name,
            total_classes=total,
            present_classes=present,
            attendance_percentage=round(pct, 2)
        ))
        
    overall_pct = (total_present_all / total_classes_all) * 100 if total_classes_all > 0 else 0.0
    
    return StudentAttendanceSummary(
        student_id=student.student_id,
        student_name=student.name,
        overall_percentage=round(overall_pct, 2),
        courses=courses_summary
    )

@router.get("/risk-analysis", response_model=RiskAnalysisResponse)
def get_attendance_risk_analysis(student_id: Optional[str] = None, limit: int = 50, db: Session = Depends(get_db)):
    """
    Scans students and estimates their risk of attendance shortage (< 75%) in their courses.
    Applies the Random Forest model to predict risk.
    """
    if student_id:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found."
              )
        students = [student]
    else:
        students = db.query(Student).limit(100).all() # Scan a subset of 100 students for performance
    
    risk_students = []
    
    for student in students:
        # Get student attendance records
        records = db.query(AttendanceRecord).filter(AttendanceRecord.student_id == student.id).all()
        if not records:
            continue
            
        # Group by course
        course_data = {}
        for r in records:
            if r.course_id not in course_data:
                course_data[r.course_id] = []
            course_data[r.course_id].append(r.status)
            
        for course_id, statuses in course_data.items():
            total = len(statuses)
            present = sum(1 for s in statuses if s == "Present")
            pct = (present / total) * 100 if total > 0 else 0.0
            
            # Predict risk if they are running borderline (< 85% attendance)
            if pct < 85.0:
                course = db.query(Course).filter(Course.id == course_id).first()
                if not course:
                    continue
                # Prepare features
                early_rate = present / total if total > 0 else 0.0
                
                # Predict
                prediction = predict_student_risk(
                    cgpa=student.cgpa,
                    semester=student.semester,
                    department=student.department,
                    early_attendance_rate=early_rate
                )
                
                if prediction["is_at_risk"]:
                    risk_students.append(RiskStudent(
                        student_id=student.student_id,
                        student_name=student.name,
                        department=student.department,
                        cgpa=student.cgpa,
                        semester=student.semester,
                        course_code=course.course_id,
                        course_name=course.course_name,
                        attendance_percentage=round(pct, 2),
                        risk_probability=round(prediction["risk_probability"] * 100, 2),
                        is_at_risk=prediction["is_at_risk"],
                        prediction_note=prediction["note"]
                    ))
                    
    # Sort by risk probability descending
    risk_students.sort(key=lambda x: x.risk_probability, reverse=True)
    
    # Apply limit
    risk_students = risk_students[:limit]
    
    return RiskAnalysisResponse(
        total_analyzed=len(students),
        total_at_risk=len(risk_students),
        risk_students=risk_students
    )

@router.post("/train-model")
def trigger_model_training(background_tasks: BackgroundTasks):
    background_tasks.add_task(train_attendance_model)
    return {"message": "Model training started in background."}
