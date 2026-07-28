from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.agents import feedback_agent

router = APIRouter(prefix="/feedback", tags=["Feedback"])

class FeedbackPayload(BaseModel):
    student_id: str
    form_id: int
    rating: float
    feedback_text: Optional[str] = ""
    faculty_id: Optional[int] = None
    course_id: Optional[int] = None

@router.post("/submit")
def submit(payload: FeedbackPayload, db: Session = Depends(get_db)):
    result = feedback_agent.submit_feedback(
        db, payload.student_id, payload.form_id, payload.rating,
        payload.feedback_text, payload.faculty_id, payload.course_id
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/analytics/faculty/{faculty_id}")
def faculty_analytics(faculty_id: int, db: Session = Depends(get_db)):
    result = feedback_agent.get_faculty_analytics(db, faculty_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/analytics/course/{course_id}")
def course_analytics(course_id: int, db: Session = Depends(get_db)):
    result = feedback_agent.get_course_analytics(db, course_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/summary")
def platform_summary(db: Session = Depends(get_db)):
    return feedback_agent.get_platform_summary(db)
