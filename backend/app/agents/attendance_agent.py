from sqlalchemy.orm import Session
from app.models.models import Student, AttendanceRecord
from loguru import logger

def handle_attendance_query(db: Session, student_id: str, entities: dict) -> dict:
    """
    Query the attendance table.
    Returns JSON dictionary.
    """
    logger.info(f"Attendance Agent: Incoming student_id={student_id}, entities={entities}")
    try:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            logger.warning(f"Attendance Agent: Student ID {student_id} not found in DB")
            return {"error": f"Student ID {student_id} not found.", "status": "No student records available"}

        query = db.query(AttendanceRecord).filter(AttendanceRecord.student_id == student.id)
        records = query.all()
        total = len(records)
        
        logger.info(f"Attendance Agent: Executed query='{query}', rows returned={total}")

        if total > 0:
            present = sum(1 for r in records if r.status == "Present")
            pct = round(present / total * 100, 1)
        else:
            logger.info("Attendance Agent: No attendance record rows. Using fallback student.attendance_percentage.")
            present = 0
            pct = student.attendance_percentage or 0.0

        status = "Safe" if pct >= 75 else "At Risk"
        return {
            "student_name": student.name,
            "total_classes": total,
            "classes_attended": present,
            "attendance_percentage": pct,
            "status": status,
            "message": "Your attendance is above the 75% requirement." if pct >= 75 else "You are at risk of shortage. Please attend all remaining classes."
        }
    except Exception as e:
        logger.exception(f"Attendance Agent error for student_id={student_id}: {e}")
        return {
            "error": f"An error occurred while fetching attendance: {str(e)}",
            "attendance_percentage": 0.0,
            "total_classes": 0,
            "classes_attended": 0,
            "status": "Error"
        }
