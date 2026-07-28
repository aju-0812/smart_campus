from sqlalchemy.orm import Session
from app.models.models import Course, Faculty, Classroom, TimetableSlot
import random

def seed_timetable(db: Session):
    print("Seeding Timetable (Zero Conflicts)...")
    courses = db.query(Course).all()
    classrooms = db.query(Classroom).filter(Classroom.is_lab == False).all()
    labs = db.query(Classroom).filter(Classroom.is_lab == True).all()
    
    if not courses or not classrooms:
        return

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
    # Periods mapping
    # 1: 08:30 - 09:20
    # 2: 09:20 - 10:10
    # 3: Tea Break 10:10 - 10:30
    # 4: 10:30 - 11:20
    # 5: 11:20 - 12:10
    # 6: Lunch 12:10 - 01:00
    # 7: 01:00 - 01:50
    # 8: 01:50 - 02:40

    periods = [
        {"num": 1, "start": "08:30", "end": "09:20", "type": "Lecture"},
        {"num": 2, "start": "09:20", "end": "10:10", "type": "Lecture"},
        {"num": 3, "start": "10:10", "end": "10:30", "type": "Tea Break"},
        {"num": 4, "start": "10:30", "end": "11:20", "type": "Lecture"},
        {"num": 5, "start": "11:20", "end": "12:10", "type": "Lecture"},
        {"num": 6, "start": "12:10", "end": "13:00", "type": "Lunch Break"},
        {"num": 7, "start": "13:00", "end": "13:50", "type": "Lecture"},
        {"num": 8, "start": "13:50", "end": "14:40", "type": "Lecture"}
    ]

    # Tracking grids to avoid conflicts
    # dict mapping: (day, period_num) -> set of (faculty_id)
    faculty_grid = {}
    # dict mapping: (day, period_num) -> set of (classroom_id)
    room_grid = {}
    
    for day in days:
        for p in periods:
            faculty_grid[(day, p["num"])] = set()
            room_grid[(day, p["num"])] = set()

    slots_to_add = []
    
    # First, schedule the breaks globally for a dummy reference if needed, 
    # but breaks don't occupy classrooms or faculty specifically. 
    # We will just generate break slots when querying or add them per classroom.
    # To save space, breaks might not even need DB rows if the frontend handles them statically.
    # However, the user specifically requested them in the timetable, so we'll add them to the section timetable.
    
    # Let's group courses by semester and department to represent "sections"
    from collections import defaultdict
    sections = defaultdict(list)
    for c in courses:
        sections[(c.department_id, c.semester)].append(c)

    for i, ((dept_id, sem), sec_courses) in enumerate(sections.items()):
        # Assign a dedicated classroom for this section deterministically
        sec_room = classrooms[i % len(classrooms)]
            
        for day in days:
            for p in periods:
                if p["type"] in ["Tea Break", "Lunch Break"]:
                    slots_to_add.append(TimetableSlot(
                        course_id=None,
                        classroom_id=sec_room.id,
                        faculty_id=sec_courses[0].faculty_id, # dummy
                        day_of_week=day,
                        start_time=p["start"],
                        end_time=p["end"],
                        semester=sem,
                        section="A",
                        slot_type=p["type"],
                        period_number=p["num"],
                        academic_year=2026
                    ))
                    continue

                # Try to pick a course for this period
                random.shuffle(sec_courses)
                scheduled = False
                for c in sec_courses:
                    fac_id = c.faculty_id
                    room_id = random.choice(labs).id if c.type == "Lab" else sec_room.id
                    
                    if fac_id not in faculty_grid[(day, p["num"])] and room_id not in room_grid[(day, p["num"])]:
                        # Schedule it
                        slots_to_add.append(TimetableSlot(
                            course_id=c.id,
                            classroom_id=room_id,
                            faculty_id=fac_id,
                            day_of_week=day,
                            start_time=p["start"],
                            end_time=p["end"],
                            semester=sem,
                            section="A",
                            slot_type=c.type,
                            period_number=p["num"],
                            academic_year=2026
                        ))
                        faculty_grid[(day, p["num"])].add(fac_id)
                        room_grid[(day, p["num"])].add(room_id)
                        scheduled = True
                        break
                        
                if not scheduled:
                    # Free period / Library hour
                    slots_to_add.append(TimetableSlot(
                        course_id=None,
                        classroom_id=sec_room.id,
                        faculty_id=sec_courses[0].faculty_id, # dummy
                        day_of_week=day,
                        start_time=p["start"],
                        end_time=p["end"],
                        semester=sem,
                        section="A",
                        slot_type="Library Hour",
                        period_number=p["num"],
                        academic_year=2026
                    ))
                    
    # Bulk save
    db.bulk_save_objects(slots_to_add)
    db.commit()
