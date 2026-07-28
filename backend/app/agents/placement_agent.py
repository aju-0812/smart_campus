"""Placement Preparation Agent — Resume scorer, company matcher, interview Q&A."""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.models import (
    Student, PlacementProfile, Skill, StudentSkill,
    Company, CompanySkillRequirement, InterviewQuestion
)
import numpy as np
from sklearn.neighbors import NearestNeighbors


def _skill_vector(skill_ids: List[int], all_skill_ids: List[int]) -> np.ndarray:
    return np.array([1 if sid in skill_ids else 0 for sid in all_skill_ids], dtype=float)


def get_placement_profile(db: Session, student_id: str) -> Dict:
    """Get full placement readiness profile for a student."""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return {"error": "Student not found"}

    profile = db.query(PlacementProfile).filter(PlacementProfile.student_id == student.id).first()
    skills = db.query(StudentSkill).filter(StudentSkill.student_id == student.id).all()

    # Compute readiness score
    cgpa_score = min(student.cgpa / 10.0 * 30, 30)  # 30 pts
    skill_score = min(len(skills) * 3, 30)  # 30 pts
    project_score = min((profile.projects if profile else 0) * 5, 15)  # 15 pts
    intern_score = min((profile.internships if profile else 0) * 7, 14)  # 14 pts
    cert_score = min((profile.certifications if profile else 0) * 2, 6)  # 6 pts
    mock_score = min((profile.mock_interviews_done if profile else 0) * 1, 5)  # 5 pts
    readiness = round(cgpa_score + skill_score + project_score + intern_score + cert_score + mock_score, 1)

    if profile:
        profile.readiness_score = readiness
        db.commit()

    skill_list = [
        {"name": ss.skill.name, "category": ss.skill.category, "proficiency": ss.proficiency}
        for ss in skills
    ]

    return {
        "student_id": student_id,
        "name": student.name,
        "department": student.department,
        "semester": student.semester,
        "cgpa": student.cgpa,
        "readiness_score": readiness,
        "resume_score": profile.resume_score if profile else 0,
        "mock_interviews_done": profile.mock_interviews_done if profile else 0,
        "internships": profile.internships if profile else 0,
        "projects": profile.projects if profile else 0,
        "certifications": profile.certifications if profile else 0,
        "linkedin_url": profile.linkedin_url if profile else None,
        "github_url": profile.github_url if profile else None,
        "skills": skill_list,
        "skill_count": len(skills),
        "score_breakdown": {
            "cgpa_score": round(cgpa_score, 1),
            "skill_score": round(skill_score, 1),
            "project_score": round(project_score, 1),
            "internship_score": round(intern_score, 1),
            "certification_score": round(cert_score, 1),
            "mock_interview_score": round(mock_score, 1),
        }
    }


def get_company_recommendations(db: Session, student_id: str, top_n: int = 8) -> List[Dict]:
    """KNN-based company recommendations by skill match."""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return []

    # Eligibility filter first (CGPA + department)
    companies = db.query(Company).all()
    eligible = [
        c for c in companies
        if student.cgpa >= c.min_cgpa and
        (c.eligible_departments == "All" or student.department in c.eligible_departments.split(","))
    ]

    if not eligible:
        return []

    all_skills = db.query(Skill).all()
    all_skill_ids = [s.id for s in all_skills]

    student_skill_ids = [ss.skill_id for ss in db.query(StudentSkill).filter(StudentSkill.student_id == student.id).all()]
    student_vec = _skill_vector(student_skill_ids, all_skill_ids)

    scored = []
    for company in eligible:
        req_skill_ids = [csr.skill_id for csr in db.query(CompanySkillRequirement).filter(CompanySkillRequirement.company_id == company.id).all()]
        company_vec = _skill_vector(req_skill_ids, all_skill_ids)

        # Cosine similarity
        denom = np.linalg.norm(student_vec) * np.linalg.norm(company_vec)
        sim = float(np.dot(student_vec, company_vec) / denom) if denom > 0 else 0.0

        matched_skills = [all_skills[i].name for i, v in enumerate(company_vec) if v > 0 and student_vec[i] > 0]
        missing_skills = [all_skills[i].name for i, v in enumerate(company_vec) if v > 0 and student_vec[i] == 0]

        scored.append({
            "company_id": company.id,
            "name": company.name,
            "industry": company.industry,
            "package_lpa_min": company.package_lpa_min,
            "package_lpa_max": company.package_lpa_max,
            "min_cgpa": company.min_cgpa,
            "match_score": round(sim * 100, 1),
            "matched_skills": matched_skills[:5],
            "missing_skills": missing_skills[:5],
            "visit_date": str(company.visit_date) if company.visit_date else None,
            "website": company.website,
        })

    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return scored[:top_n]


def get_interview_questions(db: Session, topic: Optional[str] = None, difficulty: Optional[str] = None, n: int = 10) -> List[Dict]:
    """Get interview questions filtered by topic and difficulty."""
    query = db.query(InterviewQuestion)
    if topic:
        query = query.filter(InterviewQuestion.topic.ilike(f"%{topic}%"))
    if difficulty:
        query = query.filter(InterviewQuestion.difficulty == difficulty)
    questions = query.order_by(InterviewQuestion.id).limit(n).all()

    return [
        {
            "id": q.id,
            "topic": q.topic,
            "difficulty": q.difficulty,
            "question": q.question,
            "answer": q.answer,
            "company_type": q.company_type,
        }
        for q in questions
    ]


def get_skills_gap_analysis(db: Session, student_id: str) -> Dict:
    """Analyze skills gap vs top companies in student's department."""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return {"error": "Student not found"}

    student_skill_ids = {ss.skill_id for ss in db.query(StudentSkill).filter(StudentSkill.student_id == student.id).all()}

    # Find most demanded skills across eligible companies
    companies = db.query(Company).filter(
        Company.min_cgpa <= student.cgpa
    ).all()

    skill_demand: Dict[int, int] = {}
    for company in companies:
        for csr in company.skill_requirements:
            skill_demand[csr.skill_id] = skill_demand.get(csr.skill_id, 0) + 1

    all_skills = {s.id: s for s in db.query(Skill).all()}

    # Sort by demand
    sorted_demand = sorted(skill_demand.items(), key=lambda x: x[1], reverse=True)

    have = []
    missing = []
    for skill_id, count in sorted_demand[:20]:
        skill = all_skills.get(skill_id)
        if skill:
            entry = {"name": skill.name, "category": skill.category, "demand_count": count}
            if skill_id in student_skill_ids:
                have.append(entry)
            else:
                missing.append(entry)

    return {
        "student_id": student_id,
        "skills_you_have": have[:10],
        "skills_to_learn": missing[:10],
        "completion_pct": round(len(have) / max(len(have) + len(missing), 1) * 100, 1)
    }


def get_placement_leaderboard(db: Session, department: Optional[str] = None, limit: int = 20) -> List[Dict]:
    """Top students by readiness score."""
    query = db.query(PlacementProfile, Student).join(Student, PlacementProfile.student_id == Student.id)
    if department:
        query = query.filter(Student.department == department)
    results = query.order_by(PlacementProfile.readiness_score.desc()).limit(limit).all()

    return [
        {
            "rank": i + 1,
            "student_id": student.student_id,
            "name": student.name,
            "department": student.department,
            "cgpa": student.cgpa,
            "readiness_score": profile.readiness_score,
            "projects": profile.projects,
            "internships": profile.internships,
        }
        for i, (profile, student) in enumerate(results)
    ]
