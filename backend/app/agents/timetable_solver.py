import random
from sqlalchemy.orm import Session
from app.models.models import TimetableSlot, Classroom, Course, Faculty
from loguru import logger

class TimetableScheduler:
    def __init__(self, db: Session, academic_year: int = 2026):
        self.db = db
        self.academic_year = academic_year
        self.classrooms = db.query(Classroom).all()
        self.courses = db.query(Course).all()
        self.faculties = db.query(Faculty).all()
        
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.slots = [
            "09:00", "10:00", "11:00", "12:00", 
            "13:00", "14:00", "15:00", "16:00"
        ]

    def detect_conflicts(self) -> list:
        """
        Scan all timetable slots for the active academic year and return list of conflicts.
        Conflicts include:
        1. Classroom double booking
        2. Faculty double booking
        3. Section double booking (same dept, semester, section at the same time)
        """
        slots = self.db.query(TimetableSlot).filter(
            TimetableSlot.academic_year == self.academic_year
        ).all()
        
        conflicts = []
        
        # Maps to check double booking
        classroom_occupancy = {} # (classroom_id, day, start_time) -> slot_id
        faculty_occupancy = {} # (faculty_id, day, start_time) -> slot_id
        section_occupancy = {} # (dept, semester, section, day, start_time) -> slot_id
        
        for s in slots:
            # 1. Classroom Check
            c_key = (s.classroom_id, s.day_of_week, s.start_time)
            if c_key in classroom_occupancy:
                conflicts.append({
                    "type": "Classroom Conflict",
                    "description": f"Classroom {s.classroom.room_name} double booked on {s.day_of_week} at {s.start_time}",
                    "slots": [s.id, classroom_occupancy[c_key]]
                })
            else:
                classroom_occupancy[c_key] = s.id
                
            # 2. Faculty Check
            f_key = (s.faculty_id, s.day_of_week, s.start_time)
            if f_key in faculty_occupancy:
                conflicts.append({
                    "type": "Faculty Conflict",
                    "description": f"Faculty {s.faculty.name} double booked on {s.day_of_week} at {s.start_time}",
                    "slots": [s.id, faculty_occupancy[f_key]]
                })
            else:
                faculty_occupancy[f_key] = s.id
                
            # 3. Section Check
            course = s.course
            sec_key = (course.department, s.semester, s.section, s.day_of_week, s.start_time)
            if sec_key in section_occupancy:
                conflicts.append({
                    "type": "Section Conflict",
                    "description": f"Section {course.department} Sem {s.semester} Sec {s.section} double booked on {s.day_of_week} at {s.start_time}",
                    "slots": [s.id, section_occupancy[sec_key]]
                })
            else:
                section_occupancy[sec_key] = s.id
                
        return conflicts

    def solve_csp(self, course_id: int, section: str, semester: int) -> dict:
        """
        Backtracking Constraint Satisfaction Solver to find a valid free slot for a new class.
        Finds a slot (classroom, day, time_slot) such that:
        - No classroom conflict
        - No faculty conflict
        - No section conflict
        """
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            return {"success": False, "error": "Course not found"}
            
        faculty_id = course.faculty_id
        dept = course.department
        
        # Load existing allocations into lookup sets for O(1) checks
        existing_slots = self.db.query(TimetableSlot).filter(
            TimetableSlot.academic_year == self.academic_year
        ).all()
        
        booked_classrooms = set()
        booked_faculties = set()
        booked_sections = set()
        
        for s in existing_slots:
            booked_classrooms.add((s.classroom_id, s.day_of_week, s.start_time))
            booked_faculties.add((s.faculty_id, s.day_of_week, s.start_time))
            booked_sections.add((s.course.department, s.semester, s.section, s.day_of_week, s.start_time))
            
        # Shuffle to randomize assignment and prevent clustering (resembles a Genetic Selection step)
        shuffled_classrooms = list(self.classrooms)
        random.shuffle(shuffled_classrooms)
        
        shuffled_days = list(self.days)
        random.shuffle(shuffled_days)
        
        shuffled_slots = list(self.slots)
        random.shuffle(shuffled_slots)
        
        for classroom in shuffled_classrooms:
            # Simple capacity check (heuristic: section size is ~40, capacity should be >= 40)
            if classroom.capacity < 40:
                continue
                
            for day in shuffled_days:
                for slot_time in shuffled_slots:
                    # Let's check start and end time
                    # Slot end time is start hour + 1
                    hour = int(slot_time.split(":")[0])
                    end_time = f"{hour + 1:02d}:00"
                    
                    # Check constraints
                    c_key = (classroom.id, day, slot_time)
                    f_key = (faculty_id, day, slot_time)
                    s_key = (dept, semester, section, day, slot_time)
                    
                    if c_key in booked_classrooms:
                        continue
                    if f_key in booked_faculties:
                        continue
                    if s_key in booked_sections:
                        continue
                        
                    # Found a valid assignment!
                    return {
                        "success": True,
                        "classroom_id": classroom.id,
                        "classroom_name": classroom.room_name,
                        "building": classroom.building,
                        "day_of_week": day,
                        "start_time": slot_time,
                        "end_time": end_time,
                        "academic_year": self.academic_year,
                        "section": section
                    }
                    
        return {"success": False, "error": "No conflict-free slots available."}
