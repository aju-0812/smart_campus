"""Alumni Connect Agent — KNN + cosine similarity mentor matching."""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.models import Alumni, AlumniSkill, Skill, StudentSkill, MentorshipRequest, Student, Department
from loguru import logger
import numpy as np


def _get_skill_names(db: Session) -> List[str]:
    return [s.name for s in db.query(Skill).order_by(Skill.id).all()]


def _alumni_skill_vector(db: Session, alumni: Alumni, all_skill_names: List[str]) -> np.ndarray:
    alumni_skills = {s.skill.name for s in alumni.skills if s.skill}
    return np.array([1.0 if name in alumni_skills else 0.0 for name in all_skill_names])


def _student_skill_vector(db: Session, student: Student, all_skill_names: List[str]) -> np.ndarray:
    student_skills = db.query(StudentSkill).filter(StudentSkill.student_id == student.id).all()
    student_skill_names = {ss.skill.name for ss in student_skills if ss.skill}
    return np.array([1.0 if name in student_skill_names else 0.0 for name in all_skill_names])


def _cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return float(np.dot(a, b) / (na * nb)) if na > 0 and nb > 0 else 0.0


def get_all_alumni(db: Session, department: Optional[str] = None, is_mentor: bool = True) -> List[Dict]:
    logger.info(f"Alumni Agent: get_all_alumni department={department}, is_mentor={is_mentor}")
    try:
        query = db.query(Alumni)
        if department:
            query = query.filter(Alumni.department.ilike(f"%{department}%"))
        if is_mentor:
            query = query.filter(Alumni.is_mentor == True)
        alumni_list = query.order_by(Alumni.experience_years.desc()).all()
        return [_format_alumni(a) for a in alumni_list]
    except Exception as e:
        logger.exception(f"Alumni Agent error in get_all_alumni: {e}")
        return []


def get_mentor_recommendations(db: Session, student_id: str, n: int = 6) -> List[Dict]:
    """KNN-based mentor matching using cosine similarity on skill vectors."""
    logger.info(f"Alumni Agent: get_mentor_recommendations student_id={student_id}")
    try:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            return []

        # Find department code for student
        dept_obj = db.query(Department).filter(Department.department_name == student.department).first()
        dept_code = dept_obj.department_code.upper() if dept_obj else ""

        all_skill_names = _get_skill_names(db)
        if not all_skill_names:
            logger.info("Alumni Agent: Skill master table empty. Returning top mentor list.")
            return get_all_alumni(db)[:n]

        student_vec = _student_skill_vector(db, student, all_skill_names)

        # Filter active mentors
        alumni_list = db.query(Alumni).filter(Alumni.is_mentor == True).all()

        scored = []
        for alumni in alumni_list:
            alumni_vec = _alumni_skill_vector(db, alumni, all_skill_names)
            skill_sim = _cosine_sim(student_vec, alumni_vec)

            # Department code comparison
            dept_match = alumni.department.upper() == dept_code if dept_code else False
            dept_bonus = 0.2 if dept_match else 0.0

            total_score = skill_sim + dept_bonus
            scored.append((alumni, total_score, skill_sim, dept_match))

        scored.sort(key=lambda x: x[1], reverse=True)

        result = []
        for alumni, total_score, skill_sim, dept_match in scored[:n]:
            entry = _format_alumni(alumni)
            entry["match_score"] = round(total_score * 100, 1)
            entry["skill_match_pct"] = round(skill_sim * 100, 1)
            entry["same_department"] = dept_match
            result.append(entry)

        return result
    except Exception as e:
        logger.exception(f"Alumni Agent error in get_mentor_recommendations: {e}")
        return get_all_alumni(db)[:n]


def send_mentorship_request(db: Session, student_id: str, alumni_id: int, message: str, goal: str) -> Dict:
    logger.info(f"Alumni Agent: send_mentorship_request student_id={student_id}, alumni={alumni_id}")
    try:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            return {"error": "Student not found"}

        alumni = db.query(Alumni).filter(Alumni.id == alumni_id).first()
        if not alumni:
            return {"error": "Alumni not found"}

        existing = db.query(MentorshipRequest).filter(
            MentorshipRequest.student_id == student.id,
            MentorshipRequest.alumni_id == alumni_id,
            MentorshipRequest.status == "Pending"
        ).first()
        if existing:
            return {"error": "A pending request already exists for this mentor"}

        req = MentorshipRequest(
            student_id=student.id,
            alumni_id=alumni_id,
            message=message,
            goal=goal,
            status="Pending"
        )
        db.add(req)
        db.commit()
        db.refresh(req)

        return {
            "success": True,
            "request_id": req.id,
            "alumni_name": alumni.name,
            "message": f"Mentorship request sent to {alumni.name}. They will respond via email: {alumni.email}"
        }
    except Exception as e:
        logger.exception(f"Alumni Agent error in send_mentorship_request: {e}")
        return {"error": f"Failed to send mentorship request: {str(e)}"}


def get_my_mentors(db: Session, student_id: str) -> List[Dict]:
    logger.info(f"Alumni Agent: get_my_mentors student_id={student_id}")
    try:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            return []

        requests = db.query(MentorshipRequest).filter(
            MentorshipRequest.student_id == student.id
        ).order_by(MentorshipRequest.requested_at.desc()).all()

        return [
            {
                "request_id": r.id,
                "alumni_name": r.alumni.name if r.alumni else "Unknown",
                "alumni_company": r.alumni.current_company if r.alumni else "N/A",
                "alumni_role": r.alumni.current_role if r.alumni else "N/A",
                "alumni_department": r.alumni.department if r.alumni else "N/A",
                "goal": r.goal,
                "status": r.status,
                "requested_at": str(r.requested_at)[:16] if r.requested_at else None,
            }
            for r in requests if r.alumni
        ]
    except Exception as e:
        logger.exception(f"Alumni Agent error in get_my_mentors: {e}")
        return []


def _format_alumni(a: Alumni) -> Dict:
    return {
        "id": a.id,
        "alumni_id": a.alumni_id,
        "name": a.name,
        "department": a.department,
        "graduation_year": a.graduation_year,
        "current_company": a.current_company,
        "current_role": a.current_role,
        "industry": a.industry,
        "experience_years": a.experience_years,
        "location": a.location,
        "linkedin_url": a.linkedin_url,
        "is_mentor": a.is_mentor,
        "bio": a.bio,
        "expertise_areas": a.expertise_areas.split(",") if a.expertise_areas else [],
        "skills": [s.skill.name for s in a.skills if s.skill][:8],
    }
