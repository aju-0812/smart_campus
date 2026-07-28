from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.agents import alumni_agent

router = APIRouter(prefix="/alumni", tags=["Alumni"])

class MentorshipPayload(BaseModel):
    student_id: str
    alumni_id: int
    message: str
    goal: Optional[str] = "General"

@router.get("/all")
def get_all_alumni(department: Optional[str] = None, db: Session = Depends(get_db)):
    return alumni_agent.get_all_alumni(db, department)

@router.get("/recommendations/{student_id}")
def get_recommendations(student_id: str, n: int = 6, db: Session = Depends(get_db)):
    return alumni_agent.get_mentor_recommendations(db, student_id, n)

@router.post("/request-mentorship")
def request_mentorship(payload: MentorshipPayload, db: Session = Depends(get_db)):
    result = alumni_agent.send_mentorship_request(
        db, payload.student_id, payload.alumni_id, payload.message, payload.goal
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/my-mentors/{student_id}")
def get_my_mentors(student_id: str, db: Session = Depends(get_db)):
    return alumni_agent.get_my_mentors(db, student_id)
