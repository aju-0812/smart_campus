"""Exam Discovery Agent — Schedule, hall tickets, results, countdown."""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.models import ExamSchedule, HallTicket, ExamResult, Student, Course
from datetime import date, timedelta
import math


STUDY_HOURS_PER_CREDIT = 8  # hours recommended per credit

GRADE_MAP = {
    "O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "F": 0
}

def get_exam_schedule(db: Session, student_id: str) -> Dict:
    """Get upcoming exam schedule for a student by semester."""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return {"error": "Student not found"}

    today = date.today()

    # Get exams for student's semester
    exams = db.query(ExamSchedule).filter(
        ExamSchedule.semester == student.semester,
        ExamSchedule.academic_year == 2026
    ).order_by(ExamSchedule.exam_date.asc()).all()

    upcoming = []
    past = []
    for exam in exams:
        days_left = (exam.exam_date - today).days
        entry = {
            "exam_id": exam.id,
            "course_name": exam.course.course_name,
            "course_code": exam.course.course_id,
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
            countdown_msg = f"🚨 EXAM TODAY! {next_exam['course_name']} at {next_exam['start_time']}"
        elif d == 1:
            countdown_msg = f"⚠️ Exam TOMORROW: {next_exam['course_name']}"
        else:
            countdown_msg = f"📅 Next exam in {d} days: {next_exam['course_name']} ({next_exam['date']})"

    return {
        "student_id": student_id,
        "name": student.name,
        "semester": student.semester,
        "upcoming_exams": upcoming,
        "past_exams": past,
        "total_upcoming": len(upcoming),
        "countdown": countdown_msg,
    }


def get_hall_ticket(db: Session, student_id: str) -> Dict:
    """Generate/retrieve hall tickets for a student."""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return {"error": "Student not found"}

    tickets = db.query(HallTicket).filter(HallTicket.student_id == student.id).all()
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
                "exam_type": t.exam.exam_type,
                "course": t.exam.course.course_name,
                "course_code": t.exam.course.course_id,
                "date": str(t.exam.exam_date),
                "time": f"{t.exam.start_time} – {t.exam.end_time}",
                "venue": t.exam.venue,
                "is_issued": t.is_issued,
            }
            for t in tickets
        ]
    }


def get_exam_results(db: Session, student_id: str) -> Dict:
    """Get past exam results for a student."""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return {"error": "Student not found"}

    results = db.query(ExamResult).filter(ExamResult.student_id == student.id).all()

    total_marks = sum(r.marks_obtained for r in results)
    total_max = sum(r.exam.max_marks for r in results)
    overall_pct = round((total_marks / total_max * 100) if total_max > 0 else 0, 1)

    return {
        "student_id": student_id,
        "name": student.name,
        "overall_percentage": overall_pct,
        "results": [
            {
                "exam_type": r.exam.exam_type,
                "course": r.exam.course.course_name,
                "course_code": r.exam.course.course_id,
                "date": str(r.exam.exam_date),
                "marks_obtained": r.marks_obtained,
                "max_marks": r.exam.max_marks,
                "percentage": round(r.marks_obtained / r.exam.max_marks * 100, 1),
                "grade": r.grade,
                "is_pass": r.is_pass,
            }
            for r in results
        ]
    }


def get_study_plan(db: Session, student_id: str) -> List[Dict]:
    """Generate recommended study plan based on upcoming exams."""
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
        credits = exam.course.credits or 3
        recommended_hours = STUDY_HOURS_PER_CREDIT * credits
        daily_hours = round(recommended_hours / max(days_left, 1), 1) if days_left > 0 else recommended_hours

        plan.append({
            "course": exam.course.course_name,
            "exam_date": str(exam.exam_date),
            "days_left": days_left,
            "recommended_total_hours": recommended_hours,
            "daily_hours_needed": min(daily_hours, 8),
            "urgency": "🔴 Critical" if days_left <= 3 else "🟡 Moderate" if days_left <= 7 else "🟢 Comfortable",
        })
    return plan
