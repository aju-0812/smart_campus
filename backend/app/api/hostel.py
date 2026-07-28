from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.agents import hostel_agent

router = APIRouter(prefix="/hostel", tags=["Hostel"])

class ComplaintPayload(BaseModel):
    student_id: str
    complaint_text: str

@router.get("/student/{student_id}")
def get_hostel_info(student_id: str, db: Session = Depends(get_db)):
    result = hostel_agent.get_student_hostel_info(db, student_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.post("/complaint")
def file_complaint(payload: ComplaintPayload, db: Session = Depends(get_db)):
    result = hostel_agent.file_complaint(db, payload.student_id, payload.complaint_text)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/complaints/{student_id}")
def get_complaints(student_id: str, db: Session = Depends(get_db)):
    return hostel_agent.get_complaint_history(db, student_id)

@router.get("/mess-menu")
def get_mess_menu(day: Optional[str] = None, db: Session = Depends(get_db)):
    return hostel_agent.get_mess_menu(db, day)

@router.get("/occupancy")
def get_occupancy(db: Session = Depends(get_db)):
    return hostel_agent.get_hostel_occupancy(db)
