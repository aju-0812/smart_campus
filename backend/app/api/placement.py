from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.agents import placement_agent

router = APIRouter(prefix="/placement", tags=["Placement"])

class SkillAnalysisPayload(BaseModel):
    student_id: str

@router.get("/profile/{student_id}")
def get_profile(student_id: str, db: Session = Depends(get_db)):
    result = placement_agent.get_placement_profile(db, student_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/companies/{student_id}")
def get_companies(student_id: str, top_n: int = 8, db: Session = Depends(get_db)):
    return placement_agent.get_company_recommendations(db, student_id, top_n)

@router.get("/interview-questions")
def get_questions(topic: Optional[str] = None, difficulty: Optional[str] = None, n: int = 10, db: Session = Depends(get_db)):
    return placement_agent.get_interview_questions(db, topic, difficulty, n)

@router.post("/analyze-skills")
def analyze_skills(payload: SkillAnalysisPayload, db: Session = Depends(get_db)):
    result = placement_agent.get_skills_gap_analysis(db, payload.student_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/leaderboard")
def leaderboard(department: Optional[str] = None, limit: int = 20, db: Session = Depends(get_db)):
    return placement_agent.get_placement_leaderboard(db, department, limit)
