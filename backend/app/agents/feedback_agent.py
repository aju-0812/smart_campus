"""Feedback Collection Agent — Sentiment analysis + analytics using VADER/TextBlob."""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import FeedbackForm, FeedbackResponse, Student, Faculty, Course

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False


def _analyze_sentiment(text: str) -> tuple:
    """Returns (sentiment_label, score) using TextBlob or rule-based fallback."""
    if not text or len(text.strip()) < 3:
        return "Neutral", 0.0

    if TEXTBLOB_AVAILABLE:
        polarity = TextBlob(text).sentiment.polarity
    else:
        # Simple keyword-based fallback
        positive = ["good", "great", "excellent", "helpful", "amazing", "love", "best", "clear", "wonderful"]
        negative = ["bad", "poor", "terrible", "boring", "useless", "worst", "difficult", "rude", "absent"]
        words = text.lower().split()
        pos_count = sum(1 for w in words if w in positive)
        neg_count = sum(1 for w in words if w in negative)
        polarity = (pos_count - neg_count) / max(len(words), 1) * 2

    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"

    return label, round(polarity, 4)


def submit_feedback(
    db: Session,
    student_id: str,
    form_id: int,
    rating: float,
    text: str = "",
    faculty_id: Optional[int] = None,
    course_id: Optional[int] = None,
) -> Dict:
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return {"error": "Student not found"}

    if not (1.0 <= rating <= 5.0):
        return {"error": "Rating must be between 1.0 and 5.0"}

    sentiment_label, sentiment_score = _analyze_sentiment(text)

    response = FeedbackResponse(
        form_id=form_id,
        student_id=student.id,
        faculty_id=faculty_id,
        course_id=course_id,
        rating=rating,
        feedback_text=text,
        sentiment=sentiment_label,
        sentiment_score=sentiment_score,
    )
    db.add(response)
    db.commit()
    db.refresh(response)

    return {
        "success": True,
        "response_id": response.id,
        "sentiment": sentiment_label,
        "sentiment_score": sentiment_score,
        "message": "Thank you for your feedback! It has been recorded."
    }


def get_faculty_analytics(db: Session, faculty_id: int) -> Dict:
    """Faculty-level feedback analytics."""
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not faculty:
        return {"error": "Faculty not found"}

    responses = db.query(FeedbackResponse).filter(
        FeedbackResponse.faculty_id == faculty_id
    ).all()

    if not responses:
        return {"faculty": faculty.name, "total_responses": 0, "message": "No feedback yet"}

    avg_rating = round(sum(r.rating for r in responses) / len(responses), 2)
    sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for r in responses:
        if r.sentiment in sentiments:
            sentiments[r.sentiment] += 1

    # Extract keywords from text
    all_words = []
    for r in responses:
        if r.feedback_text:
            all_words.extend(r.feedback_text.lower().split())
    stopwords = {"the", "a", "is", "in", "it", "of", "and", "to", "for", "my", "this", "very"}
    word_freq = {}
    for w in all_words:
        if w not in stopwords and len(w) > 3:
            word_freq[w] = word_freq.get(w, 0) + 1
    top_keywords = sorted(word_freq, key=word_freq.get, reverse=True)[:10]

    return {
        "faculty_id": faculty_id,
        "faculty_name": faculty.name,
        "department": faculty.department,
        "total_responses": len(responses),
        "avg_rating": avg_rating,
        "sentiment_distribution": sentiments,
        "sentiment_pct": {
            k: round(v / len(responses) * 100, 1) for k, v in sentiments.items()
        },
        "top_keywords": top_keywords,
        "rating_trend": "Improving" if avg_rating >= 4.0 else "Needs Attention" if avg_rating < 3.0 else "Stable"
    }


def get_course_analytics(db: Session, course_id: int) -> Dict:
    """Course-level feedback analytics."""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        return {"error": "Course not found"}

    responses = db.query(FeedbackResponse).filter(
        FeedbackResponse.course_id == course_id
    ).all()

    if not responses:
        return {"course": course.course_name, "total_responses": 0, "message": "No feedback yet"}

    avg_rating = round(sum(r.rating for r in responses) / len(responses), 2)
    sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for r in responses:
        if r.sentiment in sentiments:
            sentiments[r.sentiment] += 1

    return {
        "course_id": course_id,
        "course_name": course.course_name,
        "course_code": course.course_id,
        "total_responses": len(responses),
        "avg_rating": avg_rating,
        "sentiment_distribution": sentiments,
        "positive_pct": round(sentiments.get("Positive", 0) / len(responses) * 100, 1),
    }


def get_platform_summary(db: Session) -> Dict:
    """Platform-wide feedback sentiment dashboard."""
    all_responses = db.query(FeedbackResponse).all()
    total = len(all_responses)
    if total == 0:
        return {"total_responses": 0, "message": "No feedback collected yet"}

    avg_rating = round(sum(r.rating for r in all_responses) / total, 2)
    sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for r in all_responses:
        if r.sentiment in sentiments:
            sentiments[r.sentiment] += 1

    # Top-rated faculty
    faculty_ratings = {}
    for r in all_responses:
        if r.faculty_id:
            if r.faculty_id not in faculty_ratings:
                faculty_ratings[r.faculty_id] = []
            faculty_ratings[r.faculty_id].append(r.rating)

    top_faculty = []
    for fid, ratings in sorted(faculty_ratings.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True)[:5]:
        f = db.query(Faculty).filter(Faculty.id == fid).first()
        if f:
            top_faculty.append({
                "name": f.name,
                "avg_rating": round(sum(ratings) / len(ratings), 2),
                "response_count": len(ratings)
            })

    return {
        "total_responses": total,
        "avg_platform_rating": avg_rating,
        "sentiment_distribution": sentiments,
        "sentiment_pct": {k: round(v / total * 100, 1) for k, v in sentiments.items()},
        "top_rated_faculty": top_faculty,
        "overall_health": "Excellent" if avg_rating >= 4.2 else "Good" if avg_rating >= 3.5 else "Needs Attention"
    }
