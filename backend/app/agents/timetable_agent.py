from sqlalchemy.orm import Session
from app.models.models import TimetableSlot, Student, Course, Faculty, Classroom
from datetime import datetime

def handle_timetable_query(db: Session, student_id: str, entities: dict) -> dict:
    """
    Query the timetable table.
    Returns JSON dictionary.
    """
    time_filter = entities.get("time_filter")
    fac_name = entities.get("faculty_name")
    room_name = entities.get("room_name")

    if fac_name:
        fac = db.query(Faculty).filter(Faculty.faculty_name.ilike(f"%{fac_name}%")).first()
        if not fac:
            return {"error": f"Faculty {fac_name} not found."}
        slots = db.query(TimetableSlot).filter(TimetableSlot.faculty_id == fac.id).all()
        return {
            "faculty": fac.faculty_name,
            "slots": [{"day": s.day_of_week, "time": f"{s.start_time}-{s.end_time}", "course_id": s.course_id} for s in slots[:5]]
        }
        
    if room_name:
        room = db.query(Classroom).filter(Classroom.room_name.ilike(f"%{room_name}%")).first()
        if not room:
            return {"error": f"Room {room_name} not found."}
        slots = db.query(TimetableSlot).filter(TimetableSlot.classroom_id == room.id).all()
        return {
            "room": room.room_name,
            "slots": [{"day": s.day_of_week, "time": f"{s.start_time}-{s.end_time}", "course_id": s.course_id} for s in slots[:5]]
        }

    # Student timetable
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return {"error": "Student not found."}
        
    slots = db.query(TimetableSlot).filter(TimetableSlot.semester == student.semester).all()
    
    day_mapping = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    today = day_mapping.get(datetime.today().weekday(), "Monday")
    tomorrow = day_mapping.get((datetime.today().weekday() + 1) % 7, "Tuesday")

    if time_filter == "tomorrow":
        filtered = [s for s in slots if s.day_of_week == tomorrow]
    elif time_filter == "first":
        filtered = [s for s in slots if s.day_of_week == today]
        filtered.sort(key=lambda x: x.start_time)
        filtered = filtered[:1]
    elif time_filter == "afternoon":
        filtered = [s for s in slots if s.day_of_week == today and int(s.start_time.split(":")[0]) >= 12]
    else:
        # default today
        filtered = [s for s in slots if s.day_of_week == today]

    if not filtered:
        return {"message": f"No classes scheduled for {time_filter or today}."}

    results = []
    for s in filtered:
        c = db.query(Course).filter(Course.id == s.course_id).first()
        f = db.query(Faculty).filter(Faculty.id == s.faculty_id).first()
        r = db.query(Classroom).filter(Classroom.id == s.classroom_id).first()
        results.append({
            "course": c.course_name if c else "N/A",
            "faculty": f.faculty_name if f else "N/A",
            "room": r.room_name if r else "N/A",
            "time": f"{s.start_time}-{s.end_time}"
        })
        
    return {
        "student": student.name,
        "day": tomorrow if time_filter == "tomorrow" else today,
        "filter": time_filter,
        "classes": results
    }
