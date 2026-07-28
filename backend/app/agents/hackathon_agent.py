"""Hackathon Recommendation Agent — Content-based filtering on skill tags."""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.models import Hackathon, HackathonRegistration, StudentSkill, Skill, Student
from datetime import date
import numpy as np


def _skill_set(tags_str: Optional[str]) -> set:
    if not tags_str:
        return set()
    return {t.strip().lower() for t in tags_str.split(",")}


def _jaccard_similarity(set_a: set, set_b: set) -> float:
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def get_all_hackathons(db: Session, upcoming_only: bool = True) -> List[Dict]:
    """Browse all hackathons."""
    query = db.query(Hackathon)
    if upcoming_only:
        today = date.today()
        query = query.filter(
            (Hackathon.registration_deadline >= today) |
            (Hackathon.event_start_date >= today)
        )
    hackathons = query.order_by(Hackathon.registration_deadline.asc()).all()
    return [_format_hackathon(h) for h in hackathons]


def get_recommendations(db: Session, student_id: str, n: int = 8) -> List[Dict]:
    """Recommend hackathons based on student skills using Jaccard similarity."""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return []

    # Get student's skills
    student_skills = db.query(StudentSkill).filter(StudentSkill.student_id == student.id).all()
    student_skill_names = {ss.skill.name.lower() for ss in student_skills}
    student_dept = student.department.upper()

    # Get already-registered hackathon IDs
    registered_ids = {
        r.hackathon_id for r in
        db.query(HackathonRegistration).filter(HackathonRegistration.student_id == student.id).all()
    }

    today = date.today()
    hackathons = db.query(Hackathon).filter(
        (Hackathon.registration_deadline >= today) |
        (Hackathon.event_start_date >= today)
    ).all()

    scored = []
    for h in hackathons:
        if h.id in registered_ids:
            continue

        # Department eligibility
        if h.eligible_departments and h.eligible_departments != "All":
            allowed = {d.strip().upper() for d in h.eligible_departments.split(",")}
            if student_dept not in allowed:
                continue

        h_skills = _skill_set(h.skill_tags)
        sim = _jaccard_similarity(student_skill_names, h_skills)

        # Bonus for upcoming deadline urgency
        deadline_bonus = 0
        if h.registration_deadline:
            days_left = (h.registration_deadline - today).days
            if 0 <= days_left <= 7:
                deadline_bonus = 0.15

        total_score = sim + deadline_bonus
        scored.append((h, total_score))

    scored.sort(key=lambda x: x[1], reverse=True)

    result = []
    for h, score in scored[:n]:
        entry = _format_hackathon(h)
        entry["match_score"] = round(score * 100, 1)
        entry["is_registered"] = False
        result.append(entry)

    return result


def register_hackathon(db: Session, student_id: str, hackathon_id: int, team_name: str = "") -> Dict:
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return {"error": "Student not found"}

    hackathon = db.query(Hackathon).filter(Hackathon.id == hackathon_id).first()
    if not hackathon:
        return {"error": "Hackathon not found"}

    existing = db.query(HackathonRegistration).filter(
        HackathonRegistration.student_id == student.id,
        HackathonRegistration.hackathon_id == hackathon_id
    ).first()

    if existing:
        return {"error": "Already registered for this hackathon"}

    reg = HackathonRegistration(
        student_id=student.id,
        hackathon_id=hackathon_id,
        team_name=team_name or None
    )
    db.add(reg)
    db.commit()

    return {
        "success": True,
        "message": f"Successfully registered for '{hackathon.title}'",
        "registration_link": hackathon.registration_link,
    }


def get_registered_hackathons(db: Session, student_id: str) -> List[Dict]:
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return []

    regs = db.query(HackathonRegistration).filter(
        HackathonRegistration.student_id == student.id
    ).order_by(HackathonRegistration.registered_at.desc()).all()

    result = []
    for reg in regs:
        entry = _format_hackathon(reg.hackathon)
        entry["team_name"] = reg.team_name
        entry["result"] = reg.result
        entry["registered_at"] = str(reg.registered_at)[:16] if reg.registered_at else None
        result.append(entry)
    return result


def _format_hackathon(h: Hackathon) -> Dict:
    today = date.today()
    deadline_days = (h.registration_deadline - today).days if h.registration_deadline else None
    return {
        "id": h.id,
        "title": h.title,
        "organizer": h.organizer,
        "platform": h.platform,
        "mode": h.mode,
        "theme": h.theme,
        "description": h.description,
        "prize_pool": h.prize_pool,
        "team_size": f"{h.team_size_min}–{h.team_size_max}",
        "registration_deadline": str(h.registration_deadline) if h.registration_deadline else None,
        "deadline_days_left": deadline_days,
        "event_start": str(h.event_start_date) if h.event_start_date else None,
        "event_end": str(h.event_end_date) if h.event_end_date else None,
        "registration_link": h.registration_link,
        "skill_tags": h.skill_tags.split(",") if h.skill_tags else [],
        "eligible_departments": h.eligible_departments,
    }
