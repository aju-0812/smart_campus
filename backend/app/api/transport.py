from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.agents import transport_agent

router = APIRouter(prefix="/transport", tags=["Transport"])

@router.get("/buses")
def get_all_buses(db: Session = Depends(get_db)):
    return transport_agent.get_all_buses(db)

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
