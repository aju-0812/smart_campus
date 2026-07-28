from sqlalchemy.orm import Session
from app.models.models import Faculty, Department, Course
from loguru import logger

def handle_faculty_query(db: Session, entities: dict) -> dict:
    """
    Query the faculty table based on entities.
    Expects entities to have keys like 'faculty_name', 'department_name', 'course_name', 'query_type' (e.g., 'all_faculty', 'hod').
    Returns JSON dictionary with the data.
    """
    logger.info(f"Faculty Agent: Incoming entities={entities}")
    try:
        fac_name = entities.get("faculty_name")
        dept_name = entities.get("department_name")
        course_name = entities.get("course_name")
        query_type = entities.get("query_type")

        # Who teaches a specific course
        search_term = (str(course_name or "") + " " + str(dept_name or "")).strip()
        
        if search_term and not fac_name:
            # Try matching department first (e.g. "Who teaches Artificial Intelligence")
            dept = db.query(Department).filter(Department.department_name.ilike(f"%{search_term}%")).first()
            if dept:
                faculty = db.query(Faculty).filter(Faculty.department_id == dept.id).all()
                hod = db.query(Faculty).filter(Faculty.id == dept.hod_id).first() if dept.hod_id else None
                return {
                    "department": dept.department_name,
                    "hod": hod.faculty_name if hod else "N/A",
                    "faculty_members": [f.faculty_name for f in faculty[:10]]
                }
                
            # Try matching course
            course = db.query(Course).filter(Course.course_name.ilike(f"%{search_term}%")).first()
            if course:
                faculty = db.query(Faculty).filter(Faculty.id == course.faculty_id).first()
                if faculty:
                    return {
                        "course": course.course_name,
                        "faculty_name": faculty.faculty_name,
                        "designation": faculty.designation,
                        "email": faculty.email
                    }
                return {"error": f"No faculty assigned to course {course.course_name}."}

        # HOD of a department
        if query_type == "hod" and dept_name:
            dept = db.query(Department).filter(Department.department_name.ilike(f"%{dept_name}%")).first()
            if dept and dept.hod_id:
                hod = db.query(Faculty).filter(Faculty.id == dept.hod_id).first()
                if hod:
                    return {
                        "department": dept.department_name,
                        "hod_name": hod.faculty_name,
                        "qualification": hod.qualification,
                        "office_room": hod.office_room,
                        "office_building": hod.office_building
                    }
            return {"error": f"Could not find HOD for department {dept_name}."}
            
        # Faculty list for a department
        if dept_name and not fac_name:
            dept = db.query(Department).filter(Department.department_name.ilike(f"%{dept_name}%")).first()
            if dept:
                faculties = db.query(Faculty).filter(Faculty.department_id == dept.id).all()
                return {
                    "department": dept.department_name,
                    "staff": [f.faculty_name for f in faculties]
                }
            return {"error": f"Could not find department {dept_name}."}

        # Specific faculty details
        if fac_name:
            faculty = db.query(Faculty).filter(Faculty.faculty_name.ilike(f"%{fac_name}%")).first()
            if faculty:
                dept_name_str = "N/A"
                if faculty.department_id:
                    dept = db.query(Department).filter(Department.id == faculty.department_id).first()
                    if dept:
                        dept_name_str = dept.department_name

                return {
                    "faculty_name": faculty.faculty_name,
                    "designation": faculty.designation,
                    "department": dept_name_str,
                    "qualification": faculty.qualification,
                    "experience_years": faculty.experience_years,
                    "email": faculty.email,
                    "phone": faculty.phone,
                    "office_room": faculty.office_room,
                    "office_building": faculty.office_building,
                    "office_hours": faculty.office_hours
                }
            return {"error": f"Faculty {fac_name} not found."}
            
        # List all faculty
        if query_type == "all_faculty":
            facs = db.query(Faculty).all()
            return {"faculty_list": [f.faculty_name for f in facs[:20]]}

        return {"error": "Could not understand faculty query parameters."}
    except Exception as e:
        logger.exception(f"Faculty Agent error: {e}")
        return {"error": f"An error occurred while fetching faculty details: {str(e)}"}
