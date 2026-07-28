from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.agents import exam_agent

router = APIRouter(prefix="/exam", tags=["Exam"])

@router.get("/schedule/{student_id}")
def get_schedule(student_id: str, db: Session = Depends(get_db)):
    result = exam_agent.get_exam_schedule(db, student_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/hall-ticket/{student_id}")
def get_hall_ticket(student_id: str, db: Session = Depends(get_db)):
    result = exam_agent.get_hall_ticket(db, student_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/results/{student_id}")
def get_results(student_id: str, db: Session = Depends(get_db)):
    result = exam_agent.get_exam_results(db, student_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/study-plan/{student_id}")
def get_study_plan(student_id: str, db: Session = Depends(get_db)):
    return exam_agent.get_study_plan(db, student_id)
