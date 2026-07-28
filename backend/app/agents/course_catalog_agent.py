from sqlalchemy.orm import Session
from app.models.models import Course, Department

def handle_course_catalog_query(db: Session, entities: dict) -> dict:
    """
    Query the course table based on entities.
    Returns JSON dictionary.
    """
    course_name = entities.get("course_name") or ""
    dept_name = entities.get("department_name") or ""
    query_type = entities.get("query_type") or "list_courses"
    
    # Check if the text matches a department first
    search_term = (course_name + " " + dept_name).strip()
    
    if search_term:
        # 1. Try matching department
        dept = db.query(Department).filter(Department.department_name.ilike(f"%{search_term}%")).first()
        if dept:
            courses = db.query(Course).filter(Course.department_id == dept.id).all()
            return {
                "department": dept.department_name,
                "courses": [c.course_name for c in courses[:20]]
            }
            
        # 2. Try matching course directly
        course = db.query(Course).filter(Course.course_name.ilike(f"%{search_term}%")).first()
        if course:
            dept_name_str = "N/A"
            if course.department_id:
                dept_obj = db.query(Department).filter(Department.id == course.department_id).first()
                if dept_obj:
                    dept_name_str = dept_obj.department_name
                    
            return {
                "course_name": course.course_name,
                "course_id": course.course_id,
                "department": dept_name_str,
                "semester": course.semester,
                "credits": course.credits,
                "type": course.type
            }
            
        return {"error": f"Could not find any department or course matching '{search_term}'."}
        
    return {"error": "Could not understand course query parameters."}
