from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.agents import office_agent

router = APIRouter(prefix="/office", tags=["Office"])

class CertificatePayload(BaseModel):
    student_id: str
    certificate_type: str

class RequestPayload(BaseModel):
    student_id: str
    request_type: str
    remarks: Optional[str] = ""

@router.get("/fees/{student_id}")
def get_fees(student_id: str, db: Session = Depends(get_db)):
    result = office_agent.get_fee_info(db, student_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/certificates/{student_id}")
def get_certificates(student_id: str, db: Session = Depends(get_db)):
    return office_agent.get_certificates(db, student_id)

@router.post("/certificate-request")
def certificate_request(payload: CertificatePayload, db: Session = Depends(get_db)):
    result = office_agent.apply_for_certificate(db, payload.student_id, payload.certificate_type)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/requests/{student_id}")
def get_requests(student_id: str, db: Session = Depends(get_db)):
    return office_agent.get_office_requests(db, student_id)

@router.post("/request")
def submit_request(payload: RequestPayload, db: Session = Depends(get_db)):
    result = office_agent.submit_office_request(db, payload.student_id, payload.request_type, payload.remarks)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/documents/{student_id}")
def get_documents(student_id: str, db: Session = Depends(get_db)):
    return office_agent.get_office_documents(db, student_id)

@router.get("/announcements")
def get_announcements(db: Session = Depends(get_db)):
    return office_agent.get_office_announcements(db)
