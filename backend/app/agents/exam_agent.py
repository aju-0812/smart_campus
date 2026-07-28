"""Exam Discovery Agent — Schedule, hall tickets, results, countdown."""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.models import ExamSchedule, HallTicket, ExamResult, Student, Course
from loguru import logger
from datetime import date, timedelta
import math


STUDY_HOURS_PER_CREDIT = 8  # hours recommended per credit

GRADE_MAP = {
    "O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "F": 0
}

def get_exam_schedule(db: Session, student_id: str) -> Dict:
    """Get upcoming exam schedule for a student by semester."""
    logger.info(f"Exam Agent: get_exam_schedule student_id={student_id}")
    try:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            logger.warning(f"Exam Agent: Student {student_id} not found")
            return {"error": "Student not found"}

        today = date.today()

        # Get exams for student's semester
        exams = db.query(ExamSchedule).filter(
            ExamSchedule.semester == student.semester,
            ExamSchedule.academic_year == 2026
        ).order_by(ExamSchedule.exam_date.asc()).all()
        logger.info(f"Exam Agent: Found {len(exams)} exams in database for student semester={student.semester}")

        upcoming = []
        past = []
        for exam in exams:
            days_left = (exam.exam_date - today).days
            entry = {
                "exam_id": exam.id,
                "course_name": exam.course.course_name if exam.course else "N/A",
                "course_code": exam.course.course_id if exam.course else "N/A",
                "exam_type": exam.exam_type,
                "date": str(exam.exam_date),
                "start_time": exam.start_time,
                "end_time": exam.end_time,
                "venue": exam.venue,
                "max_marks": exam.max_marks,
                "days_left": days_left,
                "status": "Upcoming" if days_left >= 0 else "Completed",
            }
            if days_left >= 0:
                upcoming.append(entry)
            else:
                past.append(entry)

        # Next exam countdown
        next_exam = upcoming[0] if upcoming else None
        countdown_msg = None
        if next_exam:
            d = next_exam["days_left"]
            if d == 0:
                countdown_msg = f"EXAM TODAY! {next_exam['course_name']} at {next_exam['start_time']}"
            elif d == 1:
                countdown_msg = f"Exam TOMORROW: {next_exam['course_name']}"
            else:
                countdown_msg = f"Next exam in {d} days: {next_exam['course_name']} ({next_exam['date']})"

        return {
            "student_id": student_id,
            "name": student.name,
            "semester": student.semester,
            "upcoming_exams": upcoming,
            "past_exams": past,
            "total_upcoming": len(upcoming),
            "countdown": countdown_msg,
        }
    except Exception as e:
        logger.exception(f"Exam Agent error in get_exam_schedule: {e}")
        return {
            "student_id": student_id,
            "upcoming_exams": [],
            "past_exams": [],
            "total_upcoming": 0,
            "countdown": "No countdown available"
        }


def get_hall_ticket(db: Session, student_id: str) -> Dict:
    """Generate/retrieve hall tickets for a student."""
    logger.info(f"Exam Agent: get_hall_ticket student_id={student_id}")
    try:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            return {"error": "Student not found"}

        tickets = db.query(HallTicket).filter(HallTicket.student_id == student.id).all()
        logger.info(f"Exam Agent: Found {len(tickets)} hall tickets for student_id={student_id}")
        
        if not tickets:
            return {
                "student_id": student_id,
                "name": student.name,
                "hall_tickets": [],
                "message": "No hall tickets issued yet. Contact the exam cell."
            }

        return {
            "student_id": student_id,
            "name": student.name,
            "department": student.department,
            "semester": student.semester,
            "hall_tickets": [
                {
                    "ticket_id": f"HT-{t.id:06d}",
                    "seat_number": t.seat_number,
                    "exam_type": t.exam.exam_type if t.exam else "Semester Exam",
                    "course": t.exam.course.course_name if t.exam and t.exam.course else "N/A",
                    "course_code": t.exam.course.course_id if t.exam and t.exam.course else "N/A",
                    "date": str(t.exam.exam_date) if t.exam else "N/A",
                    "time": f"{t.exam.start_time} - {t.exam.end_time}" if t.exam else "N/A",
                    "venue": t.exam.venue if t.exam else "N/A",
                    "is_issued": t.is_issued,
                }
                for t in tickets
            ]
        }
    except Exception as e:
        logger.exception(f"Exam Agent error in get_hall_ticket: {e}")
        return {
            "student_id": student_id,
            "hall_tickets": [],
            "message": f"Error fetching hall tickets: {str(e)}"
        }


def get_exam_results(db: Session, student_id: str) -> Dict:
    """Get past exam results for a student."""
    logger.info(f"Exam Agent: get_exam_results student_id={student_id}")
    try:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            return {"error": "Student not found"}

        results = db.query(ExamResult).filter(ExamResult.student_id == student.id).all()
        logger.info(f"Exam Agent: Found {len(results)} exam results for student_id={student_id}")

        if not results:
            return {
                "student_id": student_id,
                "name": student.name,
                "overall_percentage": 0.0,
                "results": []
            }

        total_marks = sum(r.marks_obtained for r in results if r.marks_obtained is not None)
        total_max = sum(r.exam.max_marks for r in results if r.exam and r.exam.max_marks is not None)
        overall_pct = round((total_marks / total_max * 100) if total_max > 0 else 0, 1)

        return {
            "student_id": student_id,
            "name": student.name,
            "overall_percentage": overall_pct,
            "results": [
                {
                    "exam_type": r.exam.exam_type if r.exam else "Semester Exam",
                    "course": r.exam.course.course_name if r.exam and r.exam.course else "N/A",
                    "course_code": r.exam.course.course_id if r.exam and r.exam.course else "N/A",
                    "date": str(r.exam.exam_date) if r.exam else "N/A",
                    "marks_obtained": r.marks_obtained,
                    "max_marks": r.exam.max_marks if r.exam else 100,
                    "percentage": round(r.marks_obtained / r.exam.max_marks * 100, 1) if r.exam and r.exam.max_marks else 0,
                    "grade": r.grade,
                    "is_pass": r.is_pass,
                }
                for r in results
            ]
        }
    except Exception as e:
        logger.exception(f"Exam Agent error in get_exam_results: {e}")
        return {
            "student_id": student_id,
            "overall_percentage": 0.0,
            "results": []
        }


def get_study_plan(db: Session, student_id: str) -> List[Dict]:
    """Generate recommended study plan based on upcoming exams."""
    logger.info(f"Exam Agent: get_study_plan student_id={student_id}")
    try:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            return []

        today = date.today()
        exams = db.query(ExamSchedule).filter(
            ExamSchedule.semester == student.semester,
            ExamSchedule.exam_date >= today,
            ExamSchedule.academic_year == 2026
        ).order_by(ExamSchedule.exam_date.asc()).all()

        plan = []
        for exam in exams:
            days_left = (exam.exam_date - today).days
            credits = exam.course.credits if exam.course and exam.course.credits else 3
            recommended_hours = STUDY_HOURS_PER_CREDIT * credits
            daily_hours = round(recommended_hours / max(days_left, 1), 1) if days_left > 0 else recommended_hours

            plan.append({
                "course": exam.course.course_name if exam.course else "N/A",
                "exam_date": str(exam.exam_date),
                "days_left": days_left,
                "recommended_total_hours": recommended_hours,
                "daily_hours_needed": min(daily_hours, 8),
                "urgency": "🔴 Critical" if days_left <= 3 else "🟡 Moderate" if days_left <= 7 else "🟢 Comfortable",
            })
        return plan
    except Exception as e:
        logger.exception(f"Exam Agent error in get_study_plan: {e}")
        return []
