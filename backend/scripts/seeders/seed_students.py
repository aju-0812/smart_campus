from sqlalchemy.orm import Session
from app.models.models import (
    Student, Department, Hostel, HostelRoom, HostelAllocation, 
    HostelComplaint, Bus, BusStop, BusSchedule, BusDelay
)
import random
from datetime import date, timedelta
import uuid

STUDENT_FIRST_NAMES = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan", "Shaurya", "Atharv", "Ananya", "Diya", "Sana"]
STUDENT_LAST_NAMES = ["Sharma", "Verma", "Gupta", "Malhotra", "Singh", "Patel", "Reddy", "Rao", "Iyer", "Nair", "Menon", "Joshi", "Das", "Bose", "Kumar"]

def seed_students(db: Session):
    print("Seeding Students (2000 total)...")
    departments = db.query(Department).all()
    if not departments:
        return

    # First add a default user Idika Subramaniam S100001
    dept = departments[0]
    default_student = Student(
        student_id="S100001",
        name="Idika Subramaniam",
        password="test",
        department=dept.department_name,
        semester=3,
        section="A",
        cgpa=9.2,
        email="idika@smartcampus.edu",
        phone="9876543210",
        address="123 Smart St, Tech City",
        dob=date(2004, 5, 10),
        attendance_percentage=92.5
    )
    db.add(default_student)

    # Add 2000 random students
    for i in range(2, 2001):
        dept = random.choice(departments)
        fname = random.choice(STUDENT_FIRST_NAMES)
        lname = random.choice(STUDENT_LAST_NAMES)
        s = Student(
            student_id=f"S1{i:05d}",
            name=f"{fname} {lname}",
            password="test",
            department=dept.department_name,
            semester=random.randint(1, 8),
            section=random.choice(["A", "B", "C"]),
            cgpa=round(random.uniform(5.5, 9.8), 2),
            email=f"{fname.lower()}.{lname.lower()}{i}@smartcampus.edu",
            phone=f"98{random.randint(10000000, 99999999)}",
            address=f"Room {random.randint(1,500)}, Hostel Block",
            dob=date(2002, 1, 1) + timedelta(days=random.randint(0, 1500)),
            attendance_percentage=round(random.uniform(60, 100), 1)
        )
        db.add(s)
    db.commit()

    print("Seeding Hostels & Rooms...")
    hostels = [
        {"name": "Boys Hostel A", "gender": "Male", "rooms": 200},
        {"name": "Boys Hostel B", "gender": "Male", "rooms": 200},
        {"name": "Girls Hostel", "gender": "Female", "rooms": 300}
    ]
    db_hostels = []
    for h in hostels:
        hostel = Hostel(
            hostel_id=h["name"].replace(" ", "").upper(),
            name=h["name"],
            gender=h["gender"],
            total_rooms=h["rooms"],
            warden_name=f"Warden {h['name'].split()[0]}",
            warden_phone=f"9876{random.randint(100000, 999999)}"
        )
        db.add(hostel)
        db_hostels.append(hostel)
    db.commit()

    db_rooms = []
    for h in db_hostels:
        for r in range(1, h.total_rooms + 1):
            room = HostelRoom(
                hostel_id=h.id,
                room_number=f"{h.name[0]}{r}",
                floor=(r // 50) + 1,
                capacity=random.choice([1, 2, 3]),
                room_type=random.choice(["Single", "Double", "Triple"]),
                is_available=True,
                monthly_fee=random.choice([3000.0, 4500.0, 6000.0])
            )
            db.add(room)
            db_rooms.append(room)
    db.commit()

    print("Seeding Hostel Allocations...")
    all_students = db.query(Student).all()
    allocated = 0
    for s in all_students:
        if random.random() < 0.4 or s.student_id == "S100001":  # 40% hostellers
            # find an available room
            available_rooms = [r for r in db_rooms if r.is_available]
            if available_rooms:
                room = available_rooms[0]
                db.add(HostelAllocation(
                    student_id=s.id,
                    room_id=room.id,
                    check_in_date=date(2025, 8, 1),
                    is_active=True
                ))
                room.capacity -= 1
                if room.capacity == 0:
                    room.is_available = False
                allocated += 1
    db.commit()

    print("Seeding Transport (Buses)...")
    ROUTE_NAMES = [
        "Campus Express A", "Campus Express B", "City Shuttle North", "City Shuttle South", 
        "East Ring Shuttle", "West Ring Shuttle", "Railway Station Route", "Central Bus Stand Route", 
        "Tech Park Route", "Residential Colony Route", "Metro Station Link", "North Suburbs Route", 
        "South Suburbs Route", "Academic Loop", "Hostel Shuttle", "Staff Special A", 
        "Staff Special B", "Night Shuttle", "Weekend City Express", "Airport Connector"
    ]
    
    STOP_NAMES_POOL = [
        "Main Gate", "Railway Station", "Central Bus Stand", "Tech Park", "Campus Square", 
        "Admin Block Bus Stop", "Hostel Block Bus Stop", "Academic Block Circle", "Metro Junction", 
        "Central Library Bus Bay", "Sports Complex Bus Stop", "Medical College Junction", 
        "Food Court Circle", "Innovation Hub", "Science Block Stop", "West Suburb Gate", 
        "East Suburb Gate", "Hillside Colony", "Lakeview Plaza", "Town Center", "Market Square", 
        "Industrial Area Gate", "Highway Crossing", "River Road Crossing", "South Suburb Plaza", 
        "Forest Reserve Gate", "Civic Center", "Garden City Stop", "IT Park Junction"
    ]
    
    DRIVER_NAMES = [
        "Arvind Kumar", "Priya Narayanan", "Rajesh Sharma", "Suresh Patel", "Anil Deshmukh", 
        "Vikram Singh", "Sunita Nair", "Rohan Gupta", "Deepak Joshi", "Sanjay Rao", 
        "Karan Malhotra", "Amit Verma", "Neelam Mishra", "Harish Reddy", "Vijay Yadav"
    ]

    for b in range(1, 31):
        route_name = ROUTE_NAMES[(b - 1) % len(ROUTE_NAMES)]
        bus_number = f"MH12 {1000 + b * 277}-{b}"
        driver_name = DRIVER_NAMES[(b - 1) % len(DRIVER_NAMES)]
        
        bus = Bus(
            bus_number=bus_number,
            route_name=route_name,
            capacity=random.choice([40, 50, 60]),
            driver_name=driver_name,
            driver_phone=f"99{random.randint(10000000, 99999999)}",
            is_active=True
        )
        db.add(bus)
        db.flush()
        
        # Stops for this bus
        num_stops = random.randint(10, 18)
        shuffled_stops = list(STOP_NAMES_POOL)
        random.shuffle(shuffled_stops)
        bus_stops = shuffled_stops[:num_stops]
        
        for stop_idx, stop_name in enumerate(bus_stops):
            stop_order = stop_idx + 1
            minutes_offset = int((stop_idx / num_stops) * 90)
            arrival_hour = 7 + (minutes_offset // 60)
            arrival_minute = minutes_offset % 60
            
            db.add(BusStop(
                bus_id=bus.id,
                stop_name=stop_name,
                stop_order=stop_order,
                scheduled_arrival=f"{arrival_hour:02d}:{arrival_minute:02d}",
                latitude=12.97 + random.uniform(-0.02, 0.02),
                longitude=77.59 + random.uniform(-0.02, 0.02)
            ))
            
        # Add morning trip To Campus
        db.add(BusSchedule(
            bus_id=bus.id,
            direction="To Campus",
            departure_time="07:00",
            arrival_time="08:30",
            days_of_operation="Mon-Sat"
        ))
        
        # Add evening trip From Campus
        db.add(BusSchedule(
            bus_id=bus.id,
            direction="From Campus",
            departure_time="16:30",
            arrival_time="18:00",
            days_of_operation="Mon-Sat"
        ))
    db.commit()

    print("Seeding Attendance Records...")
    from app.models.models import AttendanceRecord, Course
    all_courses = db.query(Course).all()
    from collections import defaultdict
    courses_by_sem = defaultdict(list)
    for c in all_courses:
        courses_by_sem[c.semester].append(c)
        
    attendance_records = []
    start_date = date.today() - timedelta(days=50)
    
    class_dates = []
    curr = start_date
    while curr <= date.today():
        if curr.weekday() < 5:  # Mon-Fri
            class_dates.append(curr)
        curr += timedelta(days=1)
        
    for student in all_students:
        student_courses = courses_by_sem.get(student.semester, [])
        if not student_courses:
            continue
            
        target_pct = student.attendance_percentage or 80.0
        for course in student_courses:
            for dt in class_dates:
                status = "Present" if random.random() * 100 < target_pct else "Absent"
                attendance_records.append(AttendanceRecord(
                    student_id=student.id,
                    course_id=course.id,
                    date=dt,
                    status=status
                ))
                
        if len(attendance_records) >= 30000:
            db.bulk_save_objects(attendance_records)
            db.commit()
            attendance_records = []
            
    if attendance_records:
        db.bulk_save_objects(attendance_records)
        db.commit()
    print("Seeded attendance records successfully.")
