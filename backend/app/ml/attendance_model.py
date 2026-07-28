import os
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sqlalchemy.orm import Session
from app.models.models import Student, AttendanceRecord, Course, Faculty
from app.core.database import SessionLocal
from loguru import logger

MODEL_PATH = os.path.join(os.path.dirname(__file__), "attendance_rf_model.pkl")

def prepare_data(db: Session):
    logger.info("Extracting features from database for ML training...")
    
    # We want to train a model to predict if a student's final attendance in a course will be < 75%
    # Features: student's CGPA, semester, department (encoded), course department, and attendance in the first 10 classes
    
    # Query all students, attendance, courses
    students = db.query(Student).all()
    attendance_records = db.query(AttendanceRecord).all()
    courses = db.query(Course).all()
    
    if not students or not attendance_records:
        logger.warning("No data found in database. Seed the database first.")
        return None, None
        
    df_attendance = pd.DataFrame([{
        "student_id": r.student_id,
        "course_id": r.course_id,
        "date": r.date,
        "status": r.status
    } for r in attendance_records])
    
    df_students = pd.DataFrame([{
        "id": s.id,
        "cgpa": s.cgpa,
        "semester": s.semester,
        "department": s.department
    } for s in students])
    
    # Group attendance by student and course
    # Sort by date to split between "early semester" and "final outcome"
    df_attendance = df_attendance.sort_values(by="date")
    
    data_rows = []
    # For each student-course combination
    grouped = df_attendance.groupby(["student_id", "course_id"])
    
    for (student_id, course_id), group in grouped:
        if len(group) < 30:
            continue # Skip if not enough history
            
        student_info = df_students[df_students["id"] == student_id].iloc[0]
        
        # Calculate early attendance (first 10 classes)
        early_classes = group.head(10)
        early_present = (early_classes["status"] == "Present").sum()
        early_rate = early_present / len(early_classes)
        
        # Calculate overall attendance (final outcome)
        total_present = (group["status"] == "Present").sum()
        overall_rate = total_present / len(group)
        
        # Target: 1 if overall attendance is < 75% (shortage/risk), else 0
        target = 1 if overall_rate < 0.75 else 0
        
        data_rows.append({
            "cgpa": student_info["cgpa"],
            "semester": student_info["semester"],
            "department": student_info["department"],
            "early_attendance_rate": early_rate,
            "target": target
        })
        
    df = pd.DataFrame(data_rows)
    return df

def train_attendance_model():
    db = SessionLocal()
    try:
        df = prepare_data(db)
        if df is None or len(df) == 0:
            logger.error("Failed to prepare data. Seeding is required.")
            return False
            
        # One-hot encode department
        df = pd.get_dummies(df, columns=["department"], drop_first=True)
        
        X = df.drop(columns=["target"])
        y = df["target"]
        
        # Keep track of the expected feature columns
        feature_columns = list(X.columns)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        logger.info(f"Training Random Forest on {len(X_train)} samples...")
        rf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
        rf.fit(X_train, y_train)
        
        accuracy = rf.score(X_test, y_test)
        logger.info(f"Model trained with accuracy: {accuracy:.4f}")
        
        # Save model and feature list together
        with open(MODEL_PATH, "wb") as f:
            pickle.dump({
                "model": rf,
                "feature_columns": feature_columns
            }, f)
            
        logger.info(f"Model saved to {MODEL_PATH}")
        return True
    except Exception as e:
        logger.exception(f"Error training model: {e}")
        return False
    finally:
        db.close()

def predict_student_risk(cgpa: float, semester: int, department: str, early_attendance_rate: float) -> dict:
    """
    Predict attendance shortage risk for a student.
    Returns: { "is_at_risk": bool, "risk_probability": float }
    """
    if not os.path.exists(MODEL_PATH):
        # Fallback heuristic if model is not trained yet
        is_at_risk = early_attendance_rate < 0.75
        prob = 0.85 if early_attendance_rate < 0.75 else 0.15
        return {
            "is_at_risk": bool(is_at_risk),
            "risk_probability": prob,
            "note": "using heuristic fallback"
        }
        
    try:
        with open(MODEL_PATH, "rb") as f:
            data = pickle.load(f)
            model = data["model"]
            feature_columns = data["feature_columns"]
            
        # Create a single-row DataFrame for prediction
        input_data = {
            "cgpa": [cgpa],
            "semester": [semester],
            "early_attendance_rate": [early_attendance_rate]
        }
        # Add one-hot encoded departments
        for col in feature_columns:
            if col.startswith("department_"):
                dept_name = col.replace("department_", "")
                input_data[col] = [1 if department == dept_name else 0]
                
        df_input = pd.DataFrame(input_data)
        # Ensure correct column ordering
        df_input = df_input[feature_columns]
        
        prob = model.predict_proba(df_input)[0][1] # Probability of target=1 (risk)
        is_at_risk = model.predict(df_input)[0] == 1
        
        return {
            "is_at_risk": bool(is_at_risk),
            "risk_probability": float(prob),
            "note": "using Random Forest model"
        }
    except Exception as e:
        logger.error(f"Error predicting risk: {e}")
        # Return fallback heuristic
        is_at_risk = early_attendance_rate < 0.75
        prob = 0.85 if early_attendance_rate < 0.75 else 0.15
        return {
            "is_at_risk": bool(is_at_risk),
            "risk_probability": prob,
            "note": f"fallback due to error: {e}"
        }

if __name__ == "__main__":
    train_attendance_model()
