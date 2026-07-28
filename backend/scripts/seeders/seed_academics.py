from sqlalchemy.orm import Session
from app.models.models import Department, Building, Classroom, Faculty, Course
import random
import uuid

DEPARTMENTS = {
    "Artificial Intelligence & Data Science": "AIDS",
    "Computer Science": "CSE",
    "Information Technology": "IT",
    "Mechanical Engineering": "MECH",
    "Civil Engineering": "CIVIL",
    "Electrical Engineering": "EEE",
    "Electronics and Communication": "ECE",
    "Biomedical Engineering": "BME",
    "Agriculture": "AGRI",
    "Chemical Engineering": "CHEM",
    "Food Technology": "FOOD",
    "Master of Business Administration": "MBA",
    "Master of Computer Applications": "MCA",
    "Physics": "PHY",
    "Mathematics": "MATH",
    "Chemistry": "CHEM_SCI",
    "English": "ENG"
}

BUILDINGS = [
    {"name": "Admin Block", "type": "Admin", "lat": 12.9716, "lng": 77.5946},
    {"name": "Main Gate", "type": "Gate", "lat": 12.9712, "lng": 77.5940},
    {"name": "Central Library", "type": "Academic", "lat": 12.9720, "lng": 77.5950},
    {"name": "AI Block", "type": "Academic", "lat": 12.9725, "lng": 77.5955},
    {"name": "Mechanical Block", "type": "Academic", "lat": 12.9730, "lng": 77.5960},
    {"name": "Civil Block", "type": "Academic", "lat": 12.9735, "lng": 77.5965},
    {"name": "ECE Block", "type": "Academic", "lat": 12.9740, "lng": 77.5970},
    {"name": "EEE Block", "type": "Academic", "lat": 12.9745, "lng": 77.5975},
    {"name": "Auditorium", "type": "Events", "lat": 12.9750, "lng": 77.5980},
    {"name": "Sports Complex", "type": "Sports", "lat": 12.9710, "lng": 77.5985},
    {"name": "Food Court", "type": "Cafeteria", "lat": 12.9705, "lng": 77.5990},
    {"name": "Boys Hostel A", "type": "Hostel", "lat": 12.9700, "lng": 77.5995},
    {"name": "Boys Hostel B", "type": "Hostel", "lat": 12.9695, "lng": 77.5990},
    {"name": "Girls Hostel", "type": "Hostel", "lat": 12.9690, "lng": 77.5985},
    {"name": "Medical Centre", "type": "Medical", "lat": 12.9685, "lng": 77.5980},
    {"name": "Placement Cell", "type": "Admin", "lat": 12.9680, "lng": 77.5975},
    {"name": "Innovation Lab", "type": "Academic", "lat": 12.9675, "lng": 77.5970},
    {"name": "Student Activity Centre", "type": "Events", "lat": 12.9670, "lng": 77.5965},
    {"name": "Campus Temple", "type": "Misc", "lat": 12.9665, "lng": 77.5960},
    {"name": "Bus Bay", "type": "Transport", "lat": 12.9660, "lng": 77.5955}
]

FACULTY_FIRST_NAMES = ["Priya", "Arjun", "Meena", "Rahul", "Anjali", "Vikram", "Sneha", "Rohan", "Kavya", "Siddharth", "Neha", "Aditya", "Pooja", "Karan", "Shruti"]
FACULTY_LAST_NAMES = ["Raman", "Kumar", "Singh", "Sharma", "Verma", "Patel", "Reddy", "Nair", "Iyer", "Menon", "Joshi", "Das", "Bose", "Gupta", "Rao"]

DESIGNATIONS = ["Professor", "Associate Professor", "Assistant Professor", "Lecturer"]

def seed_academics(db: Session):
    print("Seeding Departments...")
    db_depts = []
    for d_name, code in DEPARTMENTS.items():
        dept = Department(department_id=code, department_name=d_name, department_code=code)
        db.add(dept)
        db_depts.append(dept)
    db.commit()

    print("Seeding Buildings...")
    db_buildings = []
    for i, b_data in enumerate(BUILDINGS):
        b = Building(
            building_code=f"BLD{i+1}",
            name=b_data["name"],
            building_type=b_data["type"],
            floors=random.randint(2, 5),
            latitude=b_data["lat"],
            longitude=b_data["lng"],
            description=f"The primary {b_data['name']} on campus."
        )
        db.add(b)
        db_buildings.append(b)
    db.commit()

    print("Seeding Classrooms...")
    room_types = ["Smart Classroom", "Seminar Hall", "Lecture Hall", "Computer Lab", "Physics Lab", "Chemistry Lab", "AI Lab"]
    academic_buildings = [b for b in db_buildings if b.building_type in ["Academic", "Admin"]]
    for b in academic_buildings:
        for r in range(1, 31):  # 30 rooms per building
            room = Classroom(
                room_name=f"{b.name.split()[0]}-{r*100 + random.randint(1,99)}",
                building=b.name,
                capacity=random.choice([30, 60, 100, 120]),
                has_smartboard=random.choice([True, False]),
                has_projector=True,
                is_lab=random.random() > 0.7,
                floor=random.randint(1, b.floors),
                room_type=random.choice(room_types)
            )
            db.add(room)
    db.commit()

    print("Seeding Faculty (20 per department)...")
    for dept in db_depts:
        for f in range(20):
            fname = random.choice(FACULTY_FIRST_NAMES)
            lname = random.choice(FACULTY_LAST_NAMES)
            designation = random.choice(DESIGNATIONS)
            faculty = Faculty(
                faculty_id=f"F{dept.department_id}{f+1:03d}",
                faculty_name=f"Dr. {fname} {lname}" if "Professor" in designation else f"{fname} {lname}",
                gender=random.choice(["Male", "Female"]),
                age=random.randint(28, 60),
                designation=designation,
                department_id=dept.id,
                qualification=random.choice(["Ph.D.", "M.Tech", "M.Sc."]),
                highest_degree=random.choice(["Ph.D.", "Master's"]),
                experience_years=random.randint(2, 30),
                email=f"{fname.lower()}.{lname.lower()}{f}.{dept.department_id.lower()}@smartcampus.edu",
                phone=f"98{random.randint(10000000, 99999999)}",
                office_room=f"Cabin {random.randint(101, 500)}",
                building=random.choice(academic_buildings).name,
                office_hours="Mon-Wed 2PM-4PM",
                research_areas="AI, Data Science" if "Intelligence" in dept.department_name else "Core Engineering",
                linkedin_url=f"https://linkedin.com/in/{fname.lower()}{lname.lower()}",
                google_scholar=f"https://scholar.google.com/{fname}{lname}",
                is_hod=(f == 0),  # First faculty is HOD
                is_dean=(f == 1)
            )
            db.add(faculty)
    db.commit()

    print("Seeding Courses...")
    db_faculty = db.query(Faculty).all()
    for dept in db_depts:
        dept_faculty = [fac for fac in db_faculty if fac.department_id == dept.id]
        if not dept_faculty:
            continue
        for sem in range(1, 9):
            for c in range(5):  # 5 courses per sem
                course_type = "Theory" if c < 3 else "Lab" if c == 3 else "Elective"
                course = Course(
                    course_id=f"{dept.department_id}{sem}0{c+1}",
                    course_name=f"{dept.department_name.split()[0]} {course_type} {sem}-{c+1}",
                    department_id=dept.id,
                    semester=sem,
                    credits=random.choice([2, 3, 4]),
                    faculty_id=random.choice(dept_faculty).id,
                    type=course_type
                )
                db.add(course)
    db.commit()
