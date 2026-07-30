"""Office Agent — Fee information, Certificate requests, Office requests, Academic documents, announcements."""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import (
    Student, FeeStatement, CertificateRequest, OfficeRequest, OfficeDocument, OfficeAnnouncement
)
from loguru import logger
from datetime import datetime, date, timedelta
import random

def get_fee_info(db: Session, student_id: str) -> Dict:
    """Get fee statement and breakdown for a student."""
    logger.info(f"Office Agent: get_fee_info student_id={student_id}")
    try:
        statement = db.query(FeeStatement).filter(FeeStatement.student_id == student_id).first()
        if not statement:
            return {
                "student_id": student_id,
                "fee_status": "No Statement",
                "message": "No active fee statement found for this student."
            }
        return {
            "student_id": student_id,
            "semester": statement.semester,
            "current_semester_fee": statement.current_semester_fee,
            "total_fee": statement.total_fee,
            "paid_amount": statement.paid_amount,
            "pending_balance": statement.pending_balance,
            "due_date": str(statement.due_date),
            "late_fee": statement.late_fee,
            "fee_breakdown": statement.fee_breakdown or {},
            "payment_history": statement.payment_history or []
        }
    except Exception as e:
        logger.exception(f"Office Agent error in get_fee_info: {e}")
        return {"error": f"Failed to fetch fee info: {str(e)}"}

def get_certificates(db: Session, student_id: str) -> List[Dict]:
    """Get certificate request history for a student."""
    logger.info(f"Office Agent: get_certificates student_id={student_id}")
    try:
        reqs = db.query(CertificateRequest).filter(
            CertificateRequest.student_id == student_id
        ).order_by(CertificateRequest.created_date.desc()).all()
        return [
            {
                "id": r.id,
                "certificate_type": r.certificate_type,
                "status": r.status,
                "application_number": r.application_number,
                "created_date": str(r.created_date)[:16] if r.created_date else None,
                "estimated_completion_date": str(r.estimated_completion_date) if r.estimated_completion_date else None,
                "remarks": r.remarks
            }
            for r in reqs
        ]
    except Exception as e:
        logger.exception(f"Office Agent error in get_certificates: {e}")
        return []

def apply_for_certificate(db: Session, student_id: str, certificate_type: str) -> Dict:
    """Submit a new certificate request."""
    logger.info(f"Office Agent: apply_for_certificate student_id={student_id} type={certificate_type}")
    try:
        app_num = f"OFF2026{random.randint(1000, 9999)}"
        est_date = date.today() + timedelta(days=5)
        
        req = CertificateRequest(
            student_id=student_id,
            certificate_type=certificate_type,
            status="Submitted",
            application_number=app_num,
            estimated_completion_date=est_date,
            remarks="Your request has been submitted successfully and is awaiting verification."
        )
        db.add(req)
        db.commit()
        db.refresh(req)
        
        return {
            "status": "Success",
            "application_number": app_num,
            "certificate_type": certificate_type,
            "estimated_completion_date": str(est_date),
            "message": f"Your request for {certificate_type} has been submitted. Application ID: {app_num}. Estimated completion: {est_date}."
        }
    except Exception as e:
        logger.exception(f"Office Agent error in apply_for_certificate: {e}")
        return {"error": f"Failed to submit request: {str(e)}"}

def get_office_requests(db: Session, student_id: str) -> List[Dict]:
    """Get general office requests for a student."""
    logger.info(f"Office Agent: get_office_requests student_id={student_id}")
    try:
        reqs = db.query(OfficeRequest).filter(
            OfficeRequest.student_id == student_id
        ).order_by(OfficeRequest.created_date.desc()).all()
        return [
            {
                "id": r.id,
                "request_type": r.request_type,
                "request_number": r.request_number,
                "status": r.status,
                "remarks": r.remarks,
                "created_date": str(r.created_date)[:16] if r.created_date else None,
                "last_updated": str(r.last_updated)[:16] if r.last_updated else None
            }
            for r in reqs
        ]
    except Exception as e:
        logger.exception(f"Office Agent error in get_office_requests: {e}")
        return []

def submit_office_request(db: Session, student_id: str, request_type: str, remarks: str = "") -> Dict:
    """Submit a general office request."""
    logger.info(f"Office Agent: submit_office_request student_id={student_id} type={request_type}")
    try:
        req_num = f"REQ2026{random.randint(1000, 9999)}"
        req = OfficeRequest(
            student_id=student_id,
            request_type=request_type,
            request_number=req_num,
            status="Pending",
            remarks=remarks or "Awaiting processing."
        )
        db.add(req)
        db.commit()
        db.refresh(req)
        
        return {
            "status": "Success",
            "request_number": req_num,
            "request_type": request_type,
            "message": f"Your request for {request_type} has been registered. Request Number: {req_num}."
        }
    except Exception as e:
        logger.exception(f"Office Agent error in submit_office_request: {e}")
        return {"error": f"Failed to submit request: {str(e)}"}

def get_office_documents(db: Session, student_id: str) -> List[Dict]:
    """Get academic and ledger documents for a student."""
    logger.info(f"Office Agent: get_office_documents student_id={student_id}")
    try:
        docs = db.query(OfficeDocument).filter(
            OfficeDocument.student_id == student_id
        ).order_by(OfficeDocument.created_date.desc()).all()
        return [
            {
                "id": d.id,
                "document_name": d.document_name,
                "document_type": d.document_type,
                "download_url": d.download_url,
                "created_date": str(d.created_date)[:10] if d.created_date else None
            }
            for d in docs
        ]
    except Exception as e:
        logger.exception(f"Office Agent error in get_office_documents: {e}")
        return []

def get_office_announcements(db: Session) -> List[Dict]:
    """Get all announcements."""
    logger.info("Office Agent: get_office_announcements")
    try:
        ann = db.query(OfficeAnnouncement).order_by(OfficeAnnouncement.publish_date.desc()).all()
        return [
            {
                "id": a.id,
                "title": a.title,
                "announcement_type": a.announcement_type,
                "content": a.content,
                "publish_date": str(a.publish_date),
                "expiry_date": str(a.expiry_date) if a.expiry_date else None
            }
            for a in ann
        ]
    except Exception as e:
        logger.exception(f"Office Agent error in get_office_announcements: {e}")
        return []

def handle_office_query(db: Session, student_id: str, query: str, entities: dict) -> dict:
    """AI Assistant Query Routing integration for Office agent."""
    q = query.lower()
    
    if any(k in q for k in ["fee", "pending", "balance", "pay"]):
        return {"fee_info": get_fee_info(db, student_id)}
        
    if any(k in q for k in ["certificate", "bonafide", "study", "conduct", "no dues", "tc"]):
        return {
            "certificate_requests": get_certificates(db, student_id),
            "available_certificates": [
                "Bonafide Certificate", "Study Certificate", "Conduct Certificate",
                "Transfer Certificate Request", "Course Completion Certificate",
                "Internship Letter", "No Dues Certificate", "Fee Paid Certificate",
                "Enrollment Certificate"
            ]
        }
        
    if any(k in q for k in ["request", "reissue", "id card", "bus pass"]):
        return {"office_requests": get_office_requests(db, student_id)}
        
    if any(k in q for k in ["document", "receipt", "ledger", "statement"]):
        return {"office_documents": get_office_documents(db, student_id)}
        
    if any(k in q for k in ["announcement", "circular", "holiday", "deadline"]):
        return {"announcements": get_office_announcements(db)}
        
    # Default complete summary
    return {
        "fee_info": get_fee_info(db, student_id),
        "certificates": get_certificates(db, student_id),
        "requests": get_office_requests(db, student_id),
        "documents": get_office_documents(db, student_id),
        "announcements": get_office_announcements(db)[:3]
    }
