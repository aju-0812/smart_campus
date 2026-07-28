from sqlalchemy.orm import Session
from app.models.models import Student, AttendanceRecord

def handle_attendance_query(db: Session, student_id: str, entities: dict) -> dict:
    """
    Query the attendance table.
    Returns JSON dictionary.
    """
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return {"error": "Student not found."}
        
    records = db.query(AttendanceRecord).filter(AttendanceRecord.student_id == student.id).all()
    total = len(records)
    present = sum(1 for r in records if r.status == "Present")
    pct = round(present / total * 100, 1) if total > 0 else 0
    status = "Safe" if pct >= 75 else "At Risk"
    
    return {
        "student_name": student.name,
        "total_classes": total,
        "classes_attended": present,
        "attendance_percentage": pct,
        "status": status,
        "message": "Your attendance is above the 75% requirement." if pct >= 75 else "You are at risk of shortage. Please attend all remaining classes."
    }
