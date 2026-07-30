from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.agents import transport_agent

router = APIRouter(prefix="/transport", tags=["Transport"])

class BookTicketPayload(BaseModel):
    student_id: str
    student_name: str
    hostel_block_room: Optional[str] = ""
    bus_id: int
    seat_number: str
    travel_date: str
    destination_city: str
    boarding_point: str
    drop_point: str
    departure_time: str
    contact_phone: str

@router.get("/buses")
def get_all_buses(city: Optional[str] = None, db: Session = Depends(get_db)):
    return transport_agent.get_all_buses(db, city)

@router.get("/route/{bus_number}")
def get_bus_stops(bus_number: str, db: Session = Depends(get_db)):
    result = transport_agent.get_bus_stops(db, bus_number)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/schedule/{bus_number}")
def get_schedule(bus_number: str, db: Session = Depends(get_db)):
    result = transport_agent.get_bus_schedule(db, bus_number)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/delay-prediction/{bus_number}")
def predict_delay(bus_number: str, db: Session = Depends(get_db)):
    result = transport_agent.predict_delay(db, bus_number)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/optimal-route")
def optimal_route(from_stop: str, to_stop: str, db: Session = Depends(get_db)):
    result = transport_agent.get_optimal_bus_route(db, from_stop, to_stop)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/seats/{bus_id}")
def get_seats_layout(bus_id: int, date: str, db: Session = Depends(get_db)):
    return transport_agent.get_seats_layout(db, bus_id, date)

@router.post("/book-ticket")
def book_ticket(payload: BookTicketPayload, db: Session = Depends(get_db)):
    result = transport_agent.book_ticket(
        db,
        student_id=payload.student_id,
        student_name=payload.student_name,
        hostel_block_room=payload.hostel_block_room,
        bus_id=payload.bus_id,
        seat_number=payload.seat_number,
        travel_date=payload.travel_date,
        destination_city=payload.destination_city,
        boarding_point=payload.boarding_point,
        drop_point=payload.drop_point,
        departure_time=payload.departure_time,
        contact_phone=payload.contact_phone
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/my-tickets/{student_id}")
def get_my_tickets(student_id: str, db: Session = Depends(get_db)):
    return transport_agent.get_student_tickets(db, student_id)

@router.post("/cancel-ticket/{ticket_id}")
def cancel_ticket(ticket_id: int, db: Session = Depends(get_db)):
    result = transport_agent.cancel_ticket(db, ticket_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
