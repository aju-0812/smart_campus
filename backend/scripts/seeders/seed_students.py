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
    for b in range(1, 31):
        bus = Bus(
            bus_number=f"MH12 {random.randint(1000, 9999)}-{b}",
            route_name=f"Route {b}",
            capacity=random.choice([40, 50, 60]),
            driver_name=random.choice(["Ramesh", "Suresh", "Mahesh", "Dinesh", "Ganesh"]),
            driver_phone=f"99{random.randint(10000000, 99999999)}",
            is_active=True
        )
        db.add(bus)
        db.flush()
        
        # Stops for this bus
        for stop_num in range(1, random.randint(15, 31)):
            db.add(BusStop(
                bus_id=bus.id,
                stop_name=f"Stop {stop_num} Area {chr(64 + (stop_num % 26 + 1))}",
                stop_order=stop_num,
                scheduled_arrival=f"{7 + (stop_num // 6):02d}:{(stop_num % 6) * 10:02d}",
                latitude=12.9 + random.uniform(-0.1, 0.1),
                longitude=77.5 + random.uniform(-0.1, 0.1)
            ))
            
        db.add(BusSchedule(
            bus_id=bus.id,
            direction="To Campus",
            departure_time="07:00",
            arrival_time="08:30",
            days_of_operation="Mon-Sat"
        ))
    db.commit()
