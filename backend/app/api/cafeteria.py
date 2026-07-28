from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.agents import cafeteria_agent

router = APIRouter(prefix="/cafeteria", tags=["Cafeteria"])

class RatingPayload(BaseModel):
    student_id: str
    food_item_id: int
    rating: float
    review: Optional[str] = ""

@router.get("/menu")
def get_menu(meal_slot: Optional[str] = None, db: Session = Depends(get_db)):
    return cafeteria_agent.get_menu_today(db, meal_slot)

@router.get("/recommendations/{student_id}")
def get_recommendations(student_id: str, method: str = "hybrid", db: Session = Depends(get_db)):
    if method == "collaborative":
        return cafeteria_agent.collaborative_recommendations(db, student_id)
    elif method == "content":
        return cafeteria_agent.content_based_recommendations(db, student_id)
    else:
        # Hybrid: merge both
        cb = cafeteria_agent.content_based_recommendations(db, student_id, 4)
        cf = cafeteria_agent.collaborative_recommendations(db, student_id, 4)
        seen_ids = set()
        merged = []
        for item in cb + cf:
            if item["food_item_id"] not in seen_ids:
                seen_ids.add(item["food_item_id"])
                merged.append(item)
        return merged[:8]

@router.post("/rate")
def submit_rating(payload: RatingPayload, db: Session = Depends(get_db)):
    result = cafeteria_agent.submit_rating(db, payload.student_id, payload.food_item_id, payload.rating, payload.review)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/nutrition/{food_item_id}")
def get_nutrition(food_item_id: int, db: Session = Depends(get_db)):
    result = cafeteria_agent.get_nutrition(db, food_item_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/top-rated")
def get_top_rated(n: int = 10, db: Session = Depends(get_db)):
    return cafeteria_agent.get_top_rated(db, n)
