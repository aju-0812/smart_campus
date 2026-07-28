from sqlalchemy.orm import Session
from app.models.models import Department, Faculty, Course
from loguru import logger

def handle_department_query(db: Session, entities: dict) -> dict:
    """
    Query the department table based on entities.
    Expects entities to have keys like 'department_name' or 'query_type' (e.g. 'all', 'medical', 'engineering').
    Returns JSON dictionary with the data.
    """
    logger.info(f"Department Agent: Incoming entities={entities}")
    try:
        dept_name = entities.get("department_name")
        query_type = entities.get("query_type")
        
        if dept_name:
            dept = db.query(Department).filter(Department.department_name.ilike(f"%{dept_name}%")).first()
            if dept:
                hod = db.query(Faculty).filter(Faculty.id == dept.hod_id).first() if dept.hod_id else None
                hod_name = hod.faculty_name if hod else "N/A"
                logger.info(f"Department Agent: Found department {dept.department_name}, hod={hod_name}")
                return {
                    "department_name": dept.department_name,
                    "department_code": dept.department_code,
                    "building": dept.building,
                    "floor": dept.floor,
                    "office_phone": dept.office_phone,
                    "office_email": dept.office_email,
                    "hod": hod_name,
                    "description": dept.description
                }
            else:
                logger.warning(f"Department Agent: No department found matching {dept_name}")
                return {"error": f"No department found matching {dept_name}."}
                
        if query_type == "all":
            depts = db.query(Department).all()
            return {"departments": [d.department_name for d in depts]}
            
        if query_type in ["engineering", "medical", "science", "commerce"]:
            depts = db.query(Department).filter(Department.description.ilike(f"%{query_type}%")).all()
            if not depts:
                return {"departments": [], "message": f"No {query_type} departments found."}
            return {"departments": [d.department_name for d in depts]}
            
        # Default fallback
        logger.warning("Department Agent: Could not determine details from query parameters.")
        return {"error": "Could not determine department details from query."}
    except Exception as e:
        logger.exception(f"Department Agent error: {e}")
        return {"error": f"An error occurred while fetching department details: {str(e)}"}
