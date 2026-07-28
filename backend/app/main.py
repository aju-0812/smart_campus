from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.models import Student
from pydantic import BaseModel

# ── Existing Routers ──────────────────────────────────────────────────────────
from app.api.timetable import router as timetable_router
from app.api.attendance import router as attendance_router

# ── New Agent Routers ─────────────────────────────────────────────────────────
from app.api.navigation import router as navigation_router
from app.api.hostel import router as hostel_router
from app.api.cafeteria import router as cafeteria_router
from app.api.placement import router as placement_router
from app.api.exam import router as exam_router
from app.api.hackathon import router as hackathon_router
from app.api.transport import router as transport_router
from app.api.feedback import router as feedback_router
from app.api.alumni import router as alumni_router

# ── Orchestrator ──────────────────────────────────────────────────────────────
from app.agents.orchestrator import query_orchestrator

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Smart Campus Autonomous Multi-Agent AI System — 11 Agents",
    version="2.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register All Routers ──────────────────────────────────────────────────────
PREFIX = settings.API_V1_STR

app.include_router(timetable_router,   prefix=PREFIX)
app.include_router(attendance_router,  prefix=PREFIX)
app.include_router(navigation_router,  prefix=PREFIX)
app.include_router(hostel_router,      prefix=PREFIX)
app.include_router(cafeteria_router,   prefix=PREFIX)
app.include_router(placement_router,   prefix=PREFIX)
app.include_router(exam_router,        prefix=PREFIX)
app.include_router(hackathon_router,   prefix=PREFIX)
app.include_router(transport_router,   prefix=PREFIX)
app.include_router(feedback_router,    prefix=PREFIX)
app.include_router(alumni_router,      prefix=PREFIX)

# ── Orchestrator Endpoint ─────────────────────────────────────────────────────
class QueryPayload(BaseModel):
    query: str
    student_id: str
    session_id: str = None

@app.post(f"{PREFIX}/orchestrator/query", tags=["Orchestrator"])
def orchestrator_query(payload: QueryPayload):
    try:
        session_id = payload.session_id or f"session_{payload.student_id}"
        response_text = query_orchestrator(payload.query, payload.student_id, session_id)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Orchestrator error: {str(e)}"
        )

# ── Auth ──────────────────────────────────────────────────────────────────────
class LoginPayload(BaseModel):
    student_id: str
    password: str

@app.post(f"{PREFIX}/auth/login", tags=["Auth"])
def login_student(payload: LoginPayload, db: Session = Depends(get_db)):
    student = db.query(Student).filter(
        (Student.student_id == payload.student_id) | (Student.email == payload.student_id)
    ).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student ID {payload.student_id} not found.")
    
    if student.password != payload.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password.")
        
    return {
        "id": student.id,
        "student_id": student.student_id,
        "name": student.name,
        "email": student.email,
        "department": student.department,
        "semester": student.semester,
        "cgpa": student.cgpa
    }

# ── Health Check ──────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def read_root():
    return {
        "message": "Smart Campus Multi-Agent AI System v2.0",
        "agents": 11,
        "docs": "/docs",
        "status": "All systems operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
