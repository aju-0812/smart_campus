from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Student, TimetableSlot, Course, Classroom, Department
from app.schemas.schemas import TimetableSlotResponse, SolveRequest, SolveResponse
from app.agents.timetable_solver import TimetableScheduler
from typing import List

router = APIRouter(prefix="/timetable", tags=["Timetable"])

@router.get("/student/{student_id}", response_model=List[TimetableSlotResponse])
def get_student_timetable(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found."
        )
        
    # Get all timetable slots for student's department, semester and year 2026
    # Note: We filter by course department since courses are departmental, and match the semester
    slots = db.query(TimetableSlot).join(Course).join(Department, Course.department_id == Department.id).filter(
        Department.department_name == student.department,
        TimetableSlot.semester == student.semester,
        TimetableSlot.academic_year == 2026
    ).all()
    
    # Sort slots based on day and time order manually or via DB
    day_order = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4}
    slots.sort(key=lambda s: (day_order.get(s.day_of_week, 5), s.start_time))
    
    return slots

@router.get("/conflicts")
def get_timetable_conflicts(db: Session = Depends(get_db)):
    scheduler = TimetableScheduler(db)
    conflicts = scheduler.detect_conflicts()
    return {
        "academic_year": 2026,
        "total_conflicts": len(conflicts),
        "conflicts": conflicts
    }

@router.post("/solve", response_model=SolveResponse)
def solve_timetable_slot(payload: SolveRequest, db: Session = Depends(get_db)):
    scheduler = TimetableScheduler(db)
    result = scheduler.solve_csp(
        course_id=payload.course_id,
        section=payload.section,
        semester=payload.semester
    )
    if not result["success"]:
        return SolveResponse(success=False, error=result["error"])
        
    # If successful, return the solved slot parameters
    return SolveResponse(
        success=True,
        classroom_id=result["classroom_id"],
        classroom_name=result["classroom_name"],
        building=result["building"],
        day_of_week=result["day_of_week"],
        start_time=result["start_time"],
        end_time=result["end_time"],
        academic_year=result["academic_year"],
        section=result["section"]
    )
