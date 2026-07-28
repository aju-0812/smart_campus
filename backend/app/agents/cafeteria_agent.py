"""Cafeteria Recommendation Agent — Content-Based + Collaborative Filtering."""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import FoodItem, CafeteriaMenu, FoodOrder, FoodRating, Student
from loguru import logger
import numpy as np
from datetime import date, timedelta


def _get_item_feature_vector(item: FoodItem) -> np.ndarray:
    """Convert food item to feature vector for content-based filtering."""
    categories = ["Main", "Snack", "Beverage", "Dessert"]
    cuisines = ["Indian", "Chinese", "Continental", "South Indian", "Fast Food"]
    cat_vec = [1 if item.category == c else 0 for c in categories]
    cui_vec = [1 if item.cuisine == c else 0 for c in cuisines]
    is_veg = [1 if item.is_veg else 0]
    price_norm = [min(item.price / 200.0, 1.0)]  # normalize 0-200 range
    cal_norm = [min((item.calories or 300) / 800.0, 1.0)]
    rating_norm = [(item.avg_rating or 3.5) / 5.0]
    return np.array(cat_vec + cui_vec + is_veg + price_norm + cal_norm + rating_norm)


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    norm_a, norm_b = np.linalg.norm(a), np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def get_menu_today(db: Session, meal_slot: Optional[str] = None) -> List[Dict]:
    """Get today's cafeteria menu."""
    logger.info(f"Cafeteria Agent: get_menu_today for meal_slot={meal_slot}")
    try:
        day = date.today().strftime("%A")
        query = db.query(CafeteriaMenu).filter(
            CafeteriaMenu.day_of_week == day,
            CafeteriaMenu.is_available == True
        )
        if meal_slot:
            query = query.filter(CafeteriaMenu.meal_slot == meal_slot)
        menus = query.all()
        logger.info(f"Cafeteria Agent: get_menu_today query='{query}', count={len(menus)}")
        
        if not menus:
            logger.info("Cafeteria Agent: Menu is empty. Falling back to top rated food items.")
            fallback_items = db.query(FoodItem).limit(10).all()
            return [
                {
                    "menu_id": item.id,
                    "food_item_id": item.id,
                    "name": item.name,
                    "category": item.category,
                    "cuisine": item.cuisine,
                    "is_veg": item.is_veg,
                    "price": item.price,
                    "calories": item.calories,
                    "avg_rating": round(item.avg_rating or 3.5, 2),
                    "meal_slot": meal_slot or "All Day",
                    "quantity_available": 20,
                    "tags": item.tags,
                }
                for item in fallback_items
            ]
            
        return [
            {
                "menu_id": m.id,
                "food_item_id": m.food_item_id,
                "name": m.food_item.name if m.food_item else "Unknown",
                "category": m.food_item.category if m.food_item else "N/A",
                "cuisine": m.food_item.cuisine if m.food_item else "N/A",
                "is_veg": m.food_item.is_veg if m.food_item else True,
                "price": m.food_item.price if m.food_item else 0.0,
                "calories": m.food_item.calories if m.food_item else 0,
                "avg_rating": round(m.food_item.avg_rating or 3.5, 2) if m.food_item else 3.5,
                "meal_slot": m.meal_slot,
                "quantity_available": m.quantity_available,
                "tags": m.food_item.tags if m.food_item else "",
            }
            for m in menus if m.food_item
        ]
    except Exception as e:
        logger.exception(f"Cafeteria Agent error in get_menu_today: {e}")
        return []


def content_based_recommendations(db: Session, student_id: str, n: int = 6) -> List[Dict]:
    """Content-based filtering: recommend based on student's order history."""
    logger.info(f"Cafeteria Agent: content_based_recommendations for student_id={student_id}")
    try:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            logger.warning(f"Cafeteria Agent: Student {student_id} not found, falling back to top rated.")
            return get_top_rated(db, n)

        past_orders = db.query(FoodOrder).filter(FoodOrder.student_id == student.id).all()
        logger.info(f"Cafeteria Agent: Found {len(past_orders)} past orders for student_id={student_id}")
        if not past_orders:
            return get_top_rated(db, n)

        ordered_ids = {o.food_item_id for o in past_orders}
        all_items = db.query(FoodItem).all()

        past_vectors = []
        for oid in ordered_ids:
            item = db.query(FoodItem).filter(FoodItem.id == oid).first()
            if item:
                past_vectors.append(_get_item_feature_vector(item))

        if not past_vectors:
            return get_top_rated(db, n)

        profile = np.mean(past_vectors, axis=0)

        candidates = [item for item in all_items if item.id not in ordered_ids]
        scored = [(item, _cosine_similarity(profile, _get_item_feature_vector(item))) for item in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)

        return _format_items(scored[:n], "Content-Based Filtering")
    except Exception as e:
        logger.exception(f"Cafeteria Agent error in content_based_recommendations: {e}")
        return get_top_rated(db, n)


def collaborative_recommendations(db: Session, student_id: str, n: int = 6) -> List[Dict]:
    """Collaborative filtering: find similar users by rating patterns."""
    logger.info(f"Cafeteria Agent: collaborative_recommendations for student_id={student_id}")
    try:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            logger.warning(f"Cafeteria Agent: Student {student_id} not found, falling back to top rated.")
            return get_top_rated(db, n)

        all_ratings = db.query(FoodRating).all()
        if not all_ratings:
            logger.warning("Cafeteria Agent: No ratings found, falling back to top rated.")
            return get_top_rated(db, n)

        user_ratings: Dict[int, Dict[int, float]] = {}
        for r in all_ratings:
            if r.student_id not in user_ratings:
                user_ratings[r.student_id] = {}
            user_ratings[r.student_id][r.food_item_id] = r.rating

        my_ratings = user_ratings.get(student.id, {})
        if not my_ratings:
            logger.info("Cafeteria Agent: No ratings for this student, falling back to top rated.")
            return get_top_rated(db, n)

        all_items_ids = list({r.food_item_id for r in all_ratings})
        def to_vec(ratings_dict):
            return np.array([ratings_dict.get(iid, 0.0) for iid in all_items_ids])

        my_vec = to_vec(my_ratings)
        similarities = []
        for uid, ratings_dict in user_ratings.items():
            if uid == student.id:
                continue
            sim = _cosine_similarity(my_vec, to_vec(ratings_dict))
            if sim > 0:
                similarities.append((uid, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        top_neighbors = similarities[:10]

        item_scores: Dict[int, float] = {}
        for uid, sim in top_neighbors:
            for item_id, rating in user_ratings[uid].items():
                if item_id not in my_ratings:
                    item_scores[item_id] = item_scores.get(item_id, 0) + sim * rating

        if not item_scores:
            return get_top_rated(db, n)

        top_item_ids = sorted(item_scores, key=item_scores.get, reverse=True)[:n]
        items = []
        for iid in top_item_ids:
            item = db.query(FoodItem).filter(FoodItem.id == iid).first()
            if item:
                items.append(item)
                
        scored = [(item, item_scores[item.id] / 10) for item in items]
        return _format_items(scored, "Collaborative Filtering")
    except Exception as e:
        logger.exception(f"Cafeteria Agent error in collaborative_recommendations: {e}")
        return get_top_rated(db, n)


def get_top_rated(db: Session, n: int = 6) -> List[Dict]:
    """Fallback: return top-rated items."""
    logger.info(f"Cafeteria Agent: get_top_rated for n={n}")
    try:
        items = db.query(FoodItem).order_by(FoodItem.avg_rating.desc()).limit(n).all()
        return _format_items([(item, item.avg_rating / 5.0 if item.avg_rating else 3.5 / 5.0) for item in items], "Top Rated")
    except Exception as e:
        logger.exception(f"Cafeteria Agent error in get_top_rated: {e}")
        return []


def _format_items(scored_items: List, method: str) -> List[Dict]:
    return [
        {
            "food_item_id": item.id,
            "name": item.name,
            "category": item.category,
            "cuisine": item.cuisine,
            "is_veg": item.is_veg,
            "price": item.price,
            "calories": item.calories,
            "avg_rating": round(item.avg_rating or 3.5, 2),
            "tags": item.tags,
            "recommendation_score": round(min(score * 100, 100), 1),
            "method": method,
        }
        for item, score in scored_items if item
    ]


def submit_rating(db: Session, student_id: str, food_item_id: int, rating: float, review: str = "") -> Dict:
    logger.info(f"Cafeteria Agent: submit_rating student_id={student_id}, item={food_item_id}, rating={rating}")
    try:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            return {"error": "Student not found"}
        if not (1.0 <= rating <= 5.0):
            return {"error": "Rating must be between 1.0 and 5.0"}

        food_rating = FoodRating(
            student_id=student.id,
            food_item_id=food_item_id,
            rating=rating,
            review=review
        )
        db.add(food_rating)

        item = db.query(FoodItem).filter(FoodItem.id == food_item_id).first()
        if item:
            avg = db.query(func.avg(FoodRating.rating)).filter(FoodRating.food_item_id == food_item_id).scalar()
            item.avg_rating = round(float(avg), 2) if avg else rating

        db.commit()
        return {"success": True, "message": f"Rating of {rating}/5 submitted for item #{food_item_id}"}
    except Exception as e:
        logger.exception(f"Cafeteria Agent error in submit_rating: {e}")
        return {"error": f"Failed to submit rating: {str(e)}"}


def get_nutrition(db: Session, food_item_id: int) -> Dict:
    logger.info(f"Cafeteria Agent: get_nutrition for food_item_id={food_item_id}")
    try:
        item = db.query(FoodItem).filter(FoodItem.id == food_item_id).first()
        if not item:
            return {"error": "Food item not found"}
        return {
            "name": item.name,
            "calories": item.calories,
            "protein_g": item.protein_g,
            "carbs_g": item.carbs_g,
            "fat_g": item.fat_g,
            "price": item.price,
            "is_veg": item.is_veg,
            "tags": item.tags,
        }
    except Exception as e:
        logger.exception(f"Cafeteria Agent error in get_nutrition: {e}")
        return {"error": f"Failed to fetch nutrition: {str(e)}"}
