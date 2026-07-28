from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.agents import navigation_agent

router = APIRouter(prefix="/navigation", tags=["Navigation"])

@router.get("/buildings")
def get_buildings(db: Session = Depends(get_db)):
    return navigation_agent.get_all_buildings(db)

@router.get("/route")
def get_route(from_building: str, to_building: str, db: Session = Depends(get_db)):
    result = navigation_agent.get_route(db, from_building, to_building)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/map")
def get_campus_map(db: Session = Depends(get_db)):
    return navigation_agent.get_campus_graph(db)
