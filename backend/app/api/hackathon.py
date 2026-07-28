from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.agents import hackathon_agent

router = APIRouter(prefix="/hackathon", tags=["Hackathon"])

class RegisterPayload(BaseModel):
    student_id: str
    hackathon_id: int
    team_name: Optional[str] = ""

@router.get("/all")
def get_all(upcoming_only: bool = True, db: Session = Depends(get_db)):
    return hackathon_agent.get_all_hackathons(db, upcoming_only)

@router.get("/recommendations/{student_id}")
def get_recommendations(student_id: str, n: int = 8, db: Session = Depends(get_db)):
    return hackathon_agent.get_recommendations(db, student_id, n)

@router.post("/register")
def register(payload: RegisterPayload, db: Session = Depends(get_db)):
    result = hackathon_agent.register_hackathon(db, payload.student_id, payload.hackathon_id, payload.team_name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/registered/{student_id}")
def get_registered(student_id: str, db: Session = Depends(get_db)):
    return hackathon_agent.get_registered_hackathons(db, student_id)
