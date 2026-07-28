"""Hostel Assistant Agent — complaint classifier + occupancy + mess menu."""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import (
    HostelAllocation, HostelRoom, Hostel, HostelComplaint, MessMenu, Student
)
import re
from datetime import datetime

# Complaint category keyword map (TF-IDF lite / rule-based)
COMPLAINT_CATEGORIES = {
    "Electrical": ["light", "fan", "electricity", "power", "switch", "socket", "bulb", "wiring", "current", "short circuit"],
    "Plumbing": ["water", "pipe", "leak", "tap", "flush", "drain", "washroom", "bathroom", "toilet", "overflow"],
    "Food": ["food", "mess", "meal", "taste", "quality", "hygiene", "cook", "dinner", "lunch", "breakfast", "rotten", "stale"],
    "Cleanliness": ["dirty", "clean", "sweep", "garbage", "dust", "cockroach", "rat", "pest", "smell", "odour", "unhygienic"],
    "Internet": ["wifi", "internet", "network", "connection", "router", "slow", "broadband"],
    "Security": ["lock", "door", "gate", "key", "lost", "theft", "stolen", "security", "guard"],
    "Furniture": ["bed", "chair", "table", "cupboard", "almirah", "broken", "mattress"],
}

def classify_complaint(text: str) -> tuple:
    """Classify complaint text into category + priority."""
    text_lower = text.lower()
    scores = {}
    for category, keywords in COMPLAINT_CATEGORIES.items():
        scores[category] = sum(1 for kw in keywords if kw in text_lower)

    best_category = max(scores, key=scores.get) if max(scores.values()) > 0 else "Other"

    # Priority scoring
    high_words = ["urgent", "emergency", "immediately", "dangerous", "broken", "no water", "no power"]
    low_words = ["minor", "small", "slight", "little"]
    priority = "High" if any(w in text_lower for w in high_words) else \
               "Low" if any(w in text_lower for w in low_words) else "Medium"

    return best_category, priority


def get_student_hostel_info(db: Session, student_id: str) -> Dict:
    """Get hostel room info for a student."""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return {"error": "Student not found"}

    allocation = db.query(HostelAllocation).filter(
        HostelAllocation.student_id == student.id,
        HostelAllocation.is_active == True
    ).first()

    if not allocation:
        return {
            "student_id": student_id,
            "name": student.name,
            "hostel_allocated": False,
            "message": "No active hostel allocation found for this student."
        }

    room = allocation.room
    hostel = room.hostel

    return {
        "student_id": student_id,
        "name": student.name,
        "hostel_allocated": True,
        "hostel_name": hostel.name,
        "hostel_gender": hostel.gender,
        "warden_name": hostel.warden_name,
        "warden_phone": hostel.warden_phone,
        "room_number": room.room_number,
        "floor": room.floor,
        "room_type": room.room_type,
        "monthly_fee": room.monthly_fee,
        "check_in_date": str(allocation.check_in_date),
    }


def file_complaint(db: Session, student_id: str, complaint_text: str) -> Dict:
    """File a new hostel complaint with auto-classification."""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return {"error": "Student not found"}

    category, priority = classify_complaint(complaint_text)

    complaint = HostelComplaint(
        student_id=student.id,
        complaint_text=complaint_text,
        category=category,
        priority=priority,
        status="Open"
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)

    return {
        "complaint_id": complaint.id,
        "status": "Filed Successfully",
        "category": category,
        "priority": priority,
        "message": f"Your complaint has been classified as '{category}' with '{priority}' priority. Tracking ID: HC-{complaint.id:04d}"
    }


def get_complaint_history(db: Session, student_id: str) -> List[Dict]:
    """Get all complaints for a student."""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return []

    complaints = db.query(HostelComplaint).filter(
        HostelComplaint.student_id == student.id
    ).order_by(HostelComplaint.created_at.desc()).all()

    return [
        {
            "id": f"HC-{c.id:04d}",
            "text": c.complaint_text,
            "category": c.category,
            "priority": c.priority,
            "status": c.status,
            "filed_at": str(c.created_at)[:16] if c.created_at else None,
            "resolved_at": str(c.resolved_at)[:16] if c.resolved_at else None,
        }
        for c in complaints
    ]


def get_mess_menu(db: Session, day: Optional[str] = None) -> List[Dict]:
    """Get mess menu for a specific day or all days."""
    query = db.query(MessMenu)
    if day:
        query = query.filter(MessMenu.day_of_week == day)
    menus = query.all()
    return [
        {
            "day": m.day_of_week,
            "meal_type": m.meal_type,
            "items": m.items,
            "calories_approx": m.calories_approx
        }
        for m in menus
    ]


def get_hostel_occupancy(db: Session) -> Dict:
    """Room occupancy statistics."""
    hostels = db.query(Hostel).all()
    result = []
    total_rooms = 0
    occupied_rooms = 0

    for hostel in hostels:
        rooms = db.query(HostelRoom).filter(HostelRoom.hostel_id == hostel.id).all()
        active_allocs = db.query(HostelAllocation).join(HostelRoom).filter(
            HostelRoom.hostel_id == hostel.id,
            HostelAllocation.is_active == True
        ).count()
        h_total = len(rooms)
        h_occ = active_allocs
        total_rooms += h_total
        occupied_rooms += h_occ
        result.append({
            "hostel": hostel.name,
            "gender": hostel.gender,
            "total_rooms": h_total,
            "occupied": h_occ,
            "available": max(0, h_total - h_occ),
            "occupancy_pct": round((h_occ / h_total * 100) if h_total > 0 else 0, 1)
        })

    return {
        "summary": {
            "total_rooms": total_rooms,
            "occupied": occupied_rooms,
            "available": total_rooms - occupied_rooms,
            "overall_occupancy_pct": round((occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0, 1)
        },
        "hostels": result
    }
