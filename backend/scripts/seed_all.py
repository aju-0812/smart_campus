"""
Master seed script for all 11 agents.
Preserves existing data (Students, Faculty, Classroom, Courses, Timetable, Attendance).
Seeds all new tables for agents 3–11.
Run: python scripts/seed_all.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import engine, Base, SessionLocal
from app.models.models import (
    Student, Faculty, Course, Skill,
    Building, CampusRoute,
    Hostel, HostelRoom, HostelAllocation, HostelComplaint, MessMenu,
    FoodItem, CafeteriaMenu, FoodOrder, FoodRating,
    StudentSkill, Company, CompanySkillRequirement, PlacementProfile, InterviewQuestion,
    ExamSchedule, HallTicket, ExamResult,
    Hackathon, HackathonRegistration,
    Bus, BusStop, BusSchedule, BusDelay,
    FeedbackForm, FeedbackResponse,
    Alumni, AlumniSkill, MentorshipRequest,
)
from faker import Faker
import random
from datetime import date, timedelta, datetime
import math

fake = Faker('en_IN')
random.seed(42)
Faker.seed(42)

DEPARTMENTS = ["CSE", "ECE", "EEE", "MECH", "CIVIL", "IT", "AIDS"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

def create_tables():
    print("🔨 Creating all new tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created.\n")

# ════════════════════════════════════════════════════════════════
#  AGENT 3 — CAMPUS NAVIGATION
# ════════════════════════════════════════════════════════════════
def seed_navigation(db: Session):
    if db.query(Building).count() > 0:
        print("⏭️  Navigation data already seeded. Skipping.")
        return

    print("🗺️  Seeding Campus Navigation data...")
    building_data = [
        ("GATE", "Main Gate", "entrance", 1, 11.0168, 76.9558),
        ("ADM", "Admin Block", "admin", 3, 11.0172, 76.9562),
        ("CSB", "CS Block", "academic", 4, 11.0175, 76.9568),
        ("ECB", "EC Block", "academic", 4, 11.0178, 76.9571),
        ("LIB", "Central Library", "library", 3, 11.0180, 76.9565),
        ("LAB1", "Computing Lab Complex", "lab", 2, 11.0176, 76.9572),
        ("CAN", "Main Cafeteria", "cafeteria", 1, 11.0170, 76.9566),
        ("HOST_M1", "Boys Hostel Block A", "hostel", 5, 11.0165, 76.9555),
        ("HOST_M2", "Boys Hostel Block B", "hostel", 5, 11.0163, 76.9553),
        ("HOST_F1", "Girls Hostel Block A", "hostel", 5, 11.0183, 76.9575),
        ("GYM", "Sports Complex & Gym", "sports", 1, 11.0174, 76.9580),
        ("MED", "Medical Center", "health", 1, 11.0169, 76.9560),
        ("MECH", "Mechanical Block", "academic", 4, 11.0182, 76.9570),
        ("CIVIL", "Civil Engineering Block", "academic", 3, 11.0185, 76.9568),
        ("AUD", "Main Auditorium", "event", 2, 11.0177, 76.9563),
        ("PARK", "Parking Area", "utility", 1, 11.0162, 76.9558),
        ("TEMP", "Temple / Prayer Hall", "utility", 1, 11.0171, 76.9574),
        ("BANK", "Campus Bank & ATM", "utility", 1, 11.0173, 76.9561),
        ("STAT", "Campus Bus Station", "transport", 1, 11.0160, 76.9556),
        ("PLAY", "Playground & Football Ground", "sports", 1, 11.0188, 76.9578),
    ]

    buildings = {}
    for code, name, btype, floors, lat, lon in building_data:
        b = Building(building_code=code, name=name, building_type=btype, floors=floors,
                     latitude=lat, longitude=lon,
                     description=f"{name} — {btype.capitalize()} facility")
        db.add(b)
        buildings[code] = b

    db.flush()

    # Create routes (adjacency graph)
    route_pairs = [
        ("GATE", "ADM", 80, 1.0),
        ("GATE", "STAT", 120, 1.5),
        ("GATE", "PARK", 100, 1.2),
        ("ADM", "CSB", 150, 1.9),
        ("ADM", "LIB", 120, 1.5),
        ("ADM", "MED", 90, 1.1),
        ("ADM", "BANK", 60, 0.75),
        ("CSB", "ECB", 100, 1.25),
        ("CSB", "LAB1", 80, 1.0),
        ("CSB", "LIB", 130, 1.6),
        ("ECB", "LAB1", 70, 0.9),
        ("ECB", "MECH", 200, 2.5),
        ("LIB", "AUD", 110, 1.4),
        ("LIB", "CAN", 90, 1.1),
        ("CAN", "HOST_M1", 180, 2.25),
        ("CAN", "HOST_F1", 200, 2.5),
        ("HOST_M1", "HOST_M2", 60, 0.75),
        ("HOST_M1", "STAT", 140, 1.75),
        ("HOST_F1", "GYM", 150, 1.9),
        ("GYM", "PLAY", 120, 1.5),
        ("MECH", "CIVIL", 100, 1.25),
        ("MECH", "GYM", 180, 2.25),
        ("AUD", "TEMP", 80, 1.0),
        ("STAT", "PARK", 80, 1.0),
        ("MED", "HOST_M1", 200, 2.5),
    ]

    for src_code, dst_code, dist, time in route_pairs:
        if src_code in buildings and dst_code in buildings:
            route = CampusRoute(
                source_id=buildings[src_code].id,
                destination_id=buildings[dst_code].id,
                distance_meters=dist,
                walk_time_minutes=time,
                path_description=f"Walk from {buildings[src_code].name} to {buildings[dst_code].name}",
                is_accessible=random.choice([True, True, True, False])
            )
            db.add(route)

    db.commit()
    print(f"   ✅ {len(building_data)} buildings, {len(route_pairs)} routes seeded.")

# ════════════════════════════════════════════════════════════════
#  AGENT 4 — HOSTEL
# ════════════════════════════════════════════════════════════════
def seed_hostel(db: Session):
    if db.query(Hostel).count() > 0:
        print("⏭️  Hostel data already seeded. Skipping.")
        return

    print("🏨 Seeding Hostel data...")
    hostels_data = [
        ("HST_M1", "Boys Hostel Block A", "Male", 150),
        ("HST_M2", "Boys Hostel Block B", "Male", 120),
        ("HST_F1", "Girls Hostel Block A", "Female", 200),
        ("HST_F2", "Girls Hostel Block B", "Female", 180),
    ]

    hostels = []
    for hid, name, gender, rooms_count in hostels_data:
        h = Hostel(
            hostel_id=hid, name=name, gender=gender, total_rooms=rooms_count,
            warden_name=fake.name(), warden_phone=f"9{random.randint(100000000,999999999)}"
        )
        db.add(h)
        hostels.append((h, rooms_count, gender))

    db.flush()

    # Rooms
    all_rooms = []
    for hostel, rooms_count, gender in hostels:
        for floor in range(1, 6):
            for room_num in range(1, rooms_count // 5 + 1):
                r_type = random.choice(["Single", "Double", "Double", "Triple"])
                cap = 1 if r_type == "Single" else (2 if r_type == "Double" else 3)
                room = HostelRoom(
                    hostel_id=hostel.id,
                    room_number=f"{floor}{room_num:02d}",
                    floor=floor,
                    capacity=cap,
                    room_type=r_type,
                    is_available=random.choice([True, False]),
                    monthly_fee=random.choice([2500.0, 3000.0, 3500.0, 4000.0])
                )
                db.add(room)
                all_rooms.append((room, gender))

    db.flush()

    # Allocate rooms to students
    students = db.query(Student).limit(500).all()
    room_idx = 0
    for student in students[:400]:
        if room_idx >= len(all_rooms):
            break
        room, gender = all_rooms[room_idx]
        alloc = HostelAllocation(
            student_id=student.id,
            room_id=room.id,
            check_in_date=date(2026, 1, 15),
            is_active=True
        )
        db.add(alloc)
        room_idx += 1

    # Mess Menu (7 days x 4 meals)
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    meals = {
        "Breakfast": ["Idli Sambar, Vada, Tea", "Dosa, Chutney, Coffee", "Poha, Upma, Juice", "Paratha, Curd, Lassi", "Pongal, Filter Coffee", "Bread Toast, Egg/Jam, Milk", "Aloo Puri, Tea"],
        "Lunch": ["Rice, Dal, Sabzi, Chapati, Salad", "Sambar Rice, Rasam, Papad", "Chicken/Paneer Curry, Rice, Roti", "Rajma, Rice, Curd Rice", "South Indian Meals Thali", "Veg/Non-Veg Biryani, Raita", "Chole Bhature, Rice, Dal"],
        "Snacks": ["Samosa, Chai", "Bread Pakoda, Juice", "Vada Pav, Coffee", "Egg Roll / Veg Roll", "Peanut Chaat, Lime Water", "Maggi, Coffee", "Biscuits, Milk"],
        "Dinner": ["Chapati, Mix Veg, Dal, Rice", "Fried Rice, Manchurian, Soup", "Roti, Paneer/Egg Bhurji, Dal", "Rice, Fish Curry/Dal Makhani", "Paratha, Aloo Sabzi, Curd", "Naan, Butter Chicken/Paneer", "Rice, Dal Fry, Raita, Pickle"],
    }
    for i, day in enumerate(days):
        for meal_type, options in meals.items():
            cal = {"Breakfast": 400, "Lunch": 750, "Snacks": 250, "Dinner": 650}[meal_type]
            mm = MessMenu(
                day_of_week=day,
                meal_type=meal_type,
                items=options[i % len(options)],
                calories_approx=cal + random.randint(-50, 100)
            )
            db.add(mm)

    # Sample complaints
    complaint_samples = [
        "The light in room 302 is not working since yesterday",
        "Water leakage from the bathroom tap, urgent fix needed",
        "Food quality in dinner was very poor today",
        "Common area is very dirty, needs immediate cleaning",
        "WiFi is extremely slow, cannot attend online classes",
        "Room door lock is broken",
        "Mattress is torn and uncomfortable",
        "Fan making loud noise, needs repair",
        "No hot water in the morning",
        "Mess serving stale food repeatedly"
    ]
    for i, text in enumerate(complaint_samples):
        from app.agents.hostel_agent import classify_complaint
        cat, pri = classify_complaint(text)
        c = HostelComplaint(
            student_id=random.choice(students[:50]).id,
            complaint_text=text,
            category=cat,
            priority=pri,
            status=random.choice(["Open", "In Progress", "Resolved", "Open"])
        )
        db.add(c)

    db.commit()
    print(f"   ✅ {len(hostels_data)} hostels, rooms, allocations, mess menus seeded.")

# ════════════════════════════════════════════════════════════════
#  AGENT 5 — CAFETERIA
# ════════════════════════════════════════════════════════════════
def seed_cafeteria(db: Session):
    if db.query(FoodItem).count() > 0:
        print("⏭️  Cafeteria data already seeded. Skipping.")
        return

    print("🍽️  Seeding Cafeteria data...")

    food_items_data = [
        # (name, category, cuisine, is_veg, price, cal, protein, carbs, fat, tags)
        ("Masala Dosa", "Main", "South Indian", True, 40, 230, 5, 40, 8, "crispy,popular"),
        ("Veg Biryani", "Main", "Indian", True, 80, 520, 12, 85, 10, "spicy,filling"),
        ("Chicken Biryani", "Main", "Indian", False, 120, 680, 35, 80, 20, "non-veg,spicy,popular"),
        ("Paneer Butter Masala + Roti", "Main", "Indian", True, 90, 580, 20, 55, 22, "rich,filling"),
        ("Egg Fried Rice", "Main", "Chinese", False, 70, 460, 15, 72, 12, "quick,popular"),
        ("Veg Fried Rice", "Main", "Chinese", True, 60, 400, 8, 70, 10, "quick,light"),
        ("Poha", "Main", "Indian", True, 25, 180, 4, 32, 5, "light,healthy,breakfast"),
        ("Upma", "Main", "South Indian", True, 25, 200, 5, 35, 6, "healthy,breakfast"),
        ("Noodles", "Main", "Chinese", True, 55, 380, 9, 60, 8, "quick,popular"),
        ("Chole Bhature", "Main", "Indian", True, 65, 540, 14, 78, 18, "heavy,spicy"),
        ("Samosa", "Snack", "Indian", True, 15, 130, 3, 18, 6, "crispy,snack"),
        ("Vada", "Snack", "South Indian", True, 20, 110, 4, 15, 5, "crispy,snack"),
        ("Bread Pakoda", "Snack", "Indian", True, 20, 140, 4, 20, 6, "snack,popular"),
        ("Egg Roll", "Snack", "Indian", False, 35, 280, 12, 30, 12, "non-veg,filling"),
        ("Puff Pastry", "Snack", "Continental", True, 25, 160, 3, 22, 8, "snack"),
        ("Maggi Noodles", "Snack", "Indian", True, 30, 320, 7, 45, 11, "quick,popular"),
        ("Masala Chai", "Beverage", "Indian", True, 10, 60, 1, 10, 2, "hot,popular"),
        ("Cold Coffee", "Beverage", "Continental", True, 40, 160, 4, 22, 6, "cold,refreshing"),
        ("Mango Lassi", "Beverage", "Indian", True, 35, 180, 5, 28, 5, "healthy,cold"),
        ("Fresh Lime Soda", "Beverage", "Indian", True, 20, 40, 0, 10, 0, "refreshing,healthy"),
        ("Chocolate Milkshake", "Beverage", "Continental", True, 50, 280, 8, 38, 10, "cold,sweet"),
        ("Gulab Jamun", "Dessert", "Indian", True, 25, 150, 2, 28, 5, "sweet,popular"),
        ("Ice Cream (Vanilla)", "Dessert", "Continental", True, 30, 130, 3, 20, 6, "cold,sweet"),
        ("Halwa", "Dessert", "Indian", True, 20, 180, 2, 30, 7, "sweet"),
        ("Fruit Salad", "Dessert", "Continental", True, 35, 120, 2, 25, 1, "healthy,light"),
        ("Payasam", "Dessert", "South Indian", True, 20, 200, 4, 35, 5, "sweet,traditional"),
        ("Rasgulla", "Dessert", "Indian", True, 20, 140, 3, 25, 4, "sweet"),
        ("Aloo Paratha + Curd", "Main", "Indian", True, 50, 420, 10, 58, 14, "filling,breakfast"),
        ("Idli (3 pcs)", "Main", "South Indian", True, 30, 160, 6, 30, 2, "healthy,light"),
        ("Fish Curry + Rice", "Main", "Indian", False, 110, 600, 38, 75, 15, "non-veg,healthy"),
    ]

    items = []
    for d in food_items_data:
        item = FoodItem(
            name=d[0], category=d[1], cuisine=d[2], is_veg=d[3],
            price=d[4], calories=d[5], protein_g=d[6], carbs_g=d[7], fat_g=d[8],
            avg_rating=round(random.uniform(3.2, 4.8), 2), tags=d[9]
        )
        db.add(item)
        items.append(item)

    db.flush()

    # Menu entries (items available on different days/slots)
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    slots = ["Breakfast","Lunch","Snacks","Dinner"]
    slot_categories = {
        "Breakfast": ["Main", "Snack", "Beverage"],
        "Lunch": ["Main", "Beverage"],
        "Snacks": ["Snack", "Beverage"],
        "Dinner": ["Main", "Dessert", "Beverage"]
    }
    for day in days:
        for slot in slots:
            allowed_cats = slot_categories[slot]
            slot_items = [i for i in items if i.category in allowed_cats]
            chosen = random.sample(slot_items, min(6, len(slot_items)))
            for item in chosen:
                menu_entry = CafeteriaMenu(
                    food_item_id=item.id, day_of_week=day, meal_slot=slot,
                    is_available=True, quantity_available=random.randint(20, 80)
                )
                db.add(menu_entry)

    # Orders and ratings from students
    students = db.query(Student).limit(200).all()
    orders_added = 0
    ratings_added = 0
    for student in students:
        # Each student ordered 3-8 items over past month
        for _ in range(random.randint(3, 8)):
            item = random.choice(items)
            qty = random.randint(1, 2)
            order = FoodOrder(
                student_id=student.id, food_item_id=item.id,
                order_date=date.today() - timedelta(days=random.randint(0, 30)),
                quantity=qty, total_price=item.price * qty
            )
            db.add(order)
            orders_added += 1

        # Ratings
        rated_items = random.sample(items, random.randint(2, 5))
        for item in rated_items:
            rating = FoodRating(
                student_id=student.id, food_item_id=item.id,
                rating=round(random.gauss(3.8, 0.7), 1),
                review=random.choice(["Great taste!", "Could be better", "Loved it!", "Okay quality", "Very fresh", ""])
            )
            db.add(rating)
            ratings_added += 1

    # Update avg_rating
    db.flush()
    from sqlalchemy import func
    for item in items:
        avg = db.query(func.avg(FoodRating.rating)).filter(FoodRating.food_item_id == item.id).scalar()
        if avg:
            item.avg_rating = round(float(avg), 2)

    db.commit()
    print(f"   ✅ {len(items)} food items, {orders_added} orders, {ratings_added} ratings seeded.")

# ════════════════════════════════════════════════════════════════
#  AGENT 6 — PLACEMENT
# ════════════════════════════════════════════════════════════════
def seed_placement(db: Session):
    if db.query(Skill).count() > 0:
        print("⏭️  Placement data already seeded. Skipping.")
        return

    print("💼 Seeding Placement data...")

    # Skills
    skills_data = [
        ("Python", "Programming"), ("Java", "Programming"), ("C++", "Programming"),
        ("JavaScript", "Programming"), ("SQL", "Programming"), ("R", "Programming"),
        ("Machine Learning", "Domain"), ("Deep Learning", "Domain"), ("Data Science", "Domain"),
        ("Natural Language Processing", "Domain"), ("Computer Vision", "Domain"),
        ("React", "Tool"), ("Node.js", "Tool"), ("Django", "Tool"), ("Spring Boot", "Tool"),
        ("Docker", "Tool"), ("Git", "Tool"), ("AWS", "Tool"), ("Linux", "Tool"),
        ("Data Structures", "Programming"), ("Algorithms", "Programming"),
        ("Database Management", "Domain"), ("Computer Networks", "Domain"),
        ("Operating Systems", "Domain"), ("System Design", "Domain"),
        ("Communication", "Soft"), ("Leadership", "Soft"), ("Teamwork", "Soft"),
        ("Problem Solving", "Soft"), ("Time Management", "Soft"),
    ]

    skills = []
    for name, cat in skills_data:
        s = Skill(name=name, category=cat)
        db.add(s)
        skills.append(s)

    db.flush()

    # Student skills
    students = db.query(Student).all()
    for student in students:
        n_skills = random.randint(3, 10)
        chosen_skills = random.sample(skills, n_skills)
        for skill in chosen_skills:
            proficiency = random.choice(["Beginner", "Beginner", "Intermediate", "Intermediate", "Advanced"])
            ss = StudentSkill(student_id=student.id, skill_id=skill.id, proficiency=proficiency)
            db.add(ss)

    db.flush()

    # Companies
    companies_data = [
        ("Google", "Technology", 25.0, 50.0, 8.0, "CSE,IT,ECE"),
        ("Microsoft", "Technology", 20.0, 45.0, 7.5, "CSE,IT,ECE"),
        ("Amazon", "E-Commerce", 18.0, 40.0, 7.0, "CSE,IT,ECE,EEE"),
        ("Infosys", "IT Services", 4.5, 8.0, 6.0, "All"),
        ("TCS", "IT Services", 3.5, 7.0, 6.0, "All"),
        ("Wipro", "IT Services", 3.5, 7.0, 6.0, "All"),
        ("Zoho", "Software", 6.0, 14.0, 7.0, "CSE,IT,ECE"),
        ("Freshworks", "SaaS", 8.0, 20.0, 7.5, "CSE,IT"),
        ("Samsung R&D", "Electronics", 10.0, 22.0, 7.5, "ECE,EEE,CSE"),
        ("ISRO", "Research", 8.0, 15.0, 8.5, "ECE,EEE,MECH,CIVIL"),
        ("L&T", "Engineering", 5.0, 12.0, 6.5, "MECH,CIVIL,EEE"),
        ("Deloitte", "Consulting", 7.0, 16.0, 7.0, "All"),
        ("Goldman Sachs", "Finance", 15.0, 35.0, 8.0, "CSE,ECE,IT"),
        ("Accenture", "IT Services", 4.5, 9.0, 6.0, "All"),
        ("Cognizant", "IT Services", 4.0, 7.5, 6.0, "All"),
    ]

    company_skill_map = {
        "Google": ["Python","Machine Learning","Data Structures","Algorithms","System Design"],
        "Microsoft": ["Python","Java","C++","System Design","Data Structures"],
        "Amazon": ["Java","Python","AWS","Data Structures","System Design"],
        "Infosys": ["Java","SQL","Communication","Teamwork","Git"],
        "TCS": ["Java","SQL","Communication","Python","Git"],
        "Wipro": ["Java","SQL","Python","Linux","Communication"],
        "Zoho": ["Java","Python","SQL","React","Django"],
        "Freshworks": ["Python","JavaScript","React","Node.js","SQL"],
        "Samsung R&D": ["C++","Algorithms","Computer Networks","Operating Systems","Linux"],
        "ISRO": ["C++","Python","Algorithms","Data Structures","Problem Solving"],
        "L&T": ["Problem Solving","Communication","Time Management","Teamwork","Leadership"],
        "Deloitte": ["SQL","Python","Communication","Leadership","Data Science"],
        "Goldman Sachs": ["Python","Algorithms","Data Structures","SQL","Problem Solving"],
        "Accenture": ["SQL","Java","Communication","Teamwork","Git"],
        "Cognizant": ["Java","SQL","Communication","Teamwork","Python"],
    }

    skill_name_map = {s.name: s for s in skills}
    companies = []
    for name, ind, pkg_min, pkg_max, min_cgpa, depts in companies_data:
        c = Company(
            name=name, industry=ind, package_lpa_min=pkg_min, package_lpa_max=pkg_max,
            min_cgpa=min_cgpa, eligible_departments=depts,
            website=f"https://www.{name.lower().replace(' ','')}.com",
            visit_date=date.today() + timedelta(days=random.randint(30, 180))
        )
        db.add(c)
        companies.append((c, name))

    db.flush()

    for company, name in companies:
        for skill_name in company_skill_map.get(name, []):
            skill = skill_name_map.get(skill_name)
            if skill:
                csr = CompanySkillRequirement(company_id=company.id, skill_id=skill.id, importance="Required")
                db.add(csr)

    db.flush()

    # Placement Profiles
    for student in students:
        pp = PlacementProfile(
            student_id=student.id,
            resume_score=round(random.uniform(50, 95), 1),
            readiness_score=0,
            mock_interviews_done=random.randint(0, 8),
            internships=random.randint(0, 2),
            projects=random.randint(0, 5),
            certifications=random.randint(0, 4),
            linkedin_url=f"https://linkedin.com/in/{fake.user_name()}" if random.random() > 0.4 else None,
            github_url=f"https://github.com/{fake.user_name()}" if random.random() > 0.3 else None,
        )
        db.add(pp)

    # Interview Questions
    iq_data = [
        ("DSA", "Easy", "What is the time complexity of binary search?", "O(log n) — it halves the search space each iteration.", "Product"),
        ("DSA", "Medium", "Explain the difference between BFS and DFS.", "BFS uses a queue and explores level by level. DFS uses a stack (or recursion) and goes deep first. BFS is better for shortest path; DFS for cycle detection.", "Product"),
        ("DSA", "Hard", "How would you design an LRU Cache?", "Use a HashMap + Doubly Linked List. HashMap gives O(1) lookup; DLL allows O(1) insert/delete at head/tail.", "Product"),
        ("OS", "Easy", "What is a deadlock? Name its four conditions.", "Deadlock: processes blocked indefinitely. Conditions: Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait.", "Service"),
        ("OS", "Medium", "What is the difference between process and thread?", "Process: independent program with own memory space. Thread: lightweight unit within a process sharing memory. Context switch for threads is faster.", "Service"),
        ("DBMS", "Easy", "What is ACID in databases?", "Atomicity, Consistency, Isolation, Durability — properties that guarantee reliable database transactions.", "Service"),
        ("DBMS", "Medium", "What is the difference between clustered and non-clustered index?", "Clustered index sorts rows physically — only one per table. Non-clustered is a separate structure pointing to rows — multiple allowed.", "Product"),
        ("CN", "Easy", "Explain the OSI model layers.", "Physical, Data Link, Network, Transport, Session, Presentation, Application — each handles a specific networking function.", "Product"),
        ("Python", "Easy", "What is a decorator in Python?", "A function that wraps another function to add behavior. Uses @syntax. Common for logging, authentication, timing.", "Startup"),
        ("Python", "Medium", "Explain list vs tuple vs set in Python.", "List: ordered, mutable. Tuple: ordered, immutable (faster). Set: unordered, unique elements, O(1) lookup.", "Startup"),
        ("ML", "Medium", "What is the bias-variance tradeoff?", "Bias: error from wrong assumptions (underfitting). Variance: sensitivity to training data (overfitting). Goal: find the sweet spot with low both.", "Product"),
        ("ML", "Hard", "How does gradient descent work?", "Iteratively adjusts parameters in the direction of steepest descent of the loss function. Learning rate controls step size. Variants: SGD, mini-batch, Adam.", "Product"),
        ("HR", "Easy", "Tell me about yourself.", "Structure: Present role/education → past experience → why this company. Keep it to 2 minutes, focused and confident.", None),
        ("HR", "Medium", "Where do you see yourself in 5 years?", "Align your growth with the company. Example: 'I want to become a strong backend engineer and lead a product team within 5 years.'", None),
        ("System Design", "Hard", "Design a URL shortening service like Bit.ly.", "Components: API server, Hash generation (base62), DB (URLs table), Cache (Redis), CDN. Handle collisions, expiry, analytics.", "Product"),
    ]
    for topic, diff, q, a, c_type in iq_data:
        db.add(InterviewQuestion(topic=topic, difficulty=diff, question=q, answer=a, company_type=c_type))

    db.commit()
    print(f"   ✅ {len(skills_data)} skills, {len(companies_data)} companies, {len(iq_data)} interview Q&As, {len(students)} placement profiles seeded.")

# ════════════════════════════════════════════════════════════════
#  AGENT 7 — EXAM
# ════════════════════════════════════════════════════════════════
def seed_exam(db: Session):
    if db.query(ExamSchedule).count() > 0:
        print("⏭️  Exam data already seeded. Skipping.")
        return

    print("📚 Seeding Exam data...")
    courses = db.query(Course).all()
    students = db.query(Student).all()

    exam_types = ["Internal1", "Internal2", "EndSem"]
    venues = ["Exam Hall 1", "Exam Hall 2", "Sports Block Hall", "Auditorium Hall A", "Auditorium Hall B"]

    exams = []
    for course in courses[:80]:  # First 80 courses
        base_date = date.today() + timedelta(days=random.randint(-30, 60))
        for i, etype in enumerate(exam_types):
            exam_date = base_date + timedelta(days=i * 25)
            exam = ExamSchedule(
                course_id=course.id,
                exam_type=etype,
                exam_date=exam_date,
                start_time=random.choice(["09:00", "10:00", "14:00", "15:00"]),
                end_time=random.choice(["12:00", "13:00", "17:00", "18:00"]),
                venue=random.choice(venues),
                semester=course.semester,
                academic_year=2026,
                max_marks=100 if etype == "EndSem" else 25
            )
            db.add(exam)
            exams.append(exam)

    db.flush()

    # Hall tickets & results
    tickets = 0
    results = 0
    for student in random.sample(students, min(200, len(students))):
        for exam in random.sample(exams, min(6, len(exams))):
            if exam.course.semester == student.semester:
                ht = HallTicket(
                    student_id=student.id, exam_id=exam.id,
                    seat_number=f"{random.choice('ABCDE')}{random.randint(1,40):02d}",
                    is_issued=True
                )
                db.add(ht)
                tickets += 1

                # Add result for past exams
                if exam.exam_date < date.today():
                    base_marks = min(100, exam.max_marks)
                    marks = round(random.gauss(base_marks * 0.72, base_marks * 0.12), 1)
                    marks = max(0, min(float(base_marks), marks))
                    pct = marks / exam.max_marks * 100
                    grade = "O" if pct>=90 else "A+" if pct>=85 else "A" if pct>=80 else "B+" if pct>=75 else "B" if pct>=65 else "C" if pct>=55 else "F"
                    result = ExamResult(
                        student_id=student.id, exam_id=exam.id,
                        marks_obtained=marks, grade=grade, is_pass=pct>=40
                    )
                    db.add(result)
                    results += 1

    db.commit()
    print(f"   ✅ {len(exams)} exam schedules, {tickets} hall tickets, {results} results seeded.")

# ════════════════════════════════════════════════════════════════
#  AGENT 8 — HACKATHON
# ════════════════════════════════════════════════════════════════
def seed_hackathon(db: Session):
    if db.query(Hackathon).count() > 0:
        print("⏭️  Hackathon data already seeded. Skipping.")
        return

    print("🚀 Seeding Hackathon data...")

    hackathons_data = [
        ("Smart India Hackathon 2026", "MoE / AICTE", "Unstop", "Offline", "Government & Social Impact", "₹1,00,000", 2, 6, 10, "Python,ML,IoT,Web", "All"),
        ("HackWithInfy", "Infosys", "Devfolio", "Online", "Enterprise Tech", "₹50,000", 2, 4, 15, "Java,SQL,React,Python", "CSE,IT,ECE"),
        ("Smart Campus Ideathon", "AICTE", "Unstop", "Hybrid", "EdTech & Campus", "₹30,000", 1, 4, 20, "ML,Python,React,AI", "All"),
        ("Google Gemini AI Sprint", "Google", "Devfolio", "Online", "AI & LLM", "₹2,00,000", 1, 3, 7, "Python,ML,NLP,Gemini", "CSE,IT,AIDS"),
        ("Microsoft Imagine Cup", "Microsoft", "Devfolio", "Online", "Social Impact", "Global Prize Pool", 1, 4, 30, "Azure,Python,ML,React", "All"),
        ("Flipkart Grid 6.0", "Flipkart", "Unstop", "Online", "E-Commerce & Retail", "₹75,000", 2, 3, 5, "Python,ML,Data Science,SQL", "CSE,IT,ECE"),
        ("HackerEarth ML Challenge", "HackerEarth", "HackerEarth", "Online", "Machine Learning", "₹25,000", 1, 1, 14, "Python,ML,Deep Learning,Data Science", "CSE,IT,AIDS"),
        ("Myntra HackerRamp", "Myntra", "HackerEarth", "Hybrid", "Fashion Tech", "₹1,50,000", 2, 4, 8, "Python,ML,React,Node.js", "CSE,IT"),
        ("IoT Innovation Challenge", "IIT Bombay", "Devfolio", "Offline", "Internet of Things", "₹80,000", 2, 4, 18, "Python,IoT,C++,Embedded", "ECE,EEE,CSE"),
        ("Blockchain Summit Hackathon", "Chainlink", "Devfolio", "Online", "Web3 & Blockchain", "₹3,00,000", 1, 4, 12, "Blockchain,Python,Solidity", "CSE,IT"),
        ("Zomato FoodTech Hack", "Zomato", "Unstop", "Online", "Food & Logistics", "₹60,000", 2, 4, 6, "Python,ML,React,SQL", "CSE,IT,AIDS"),
        ("ISRO Space Hackathon", "ISRO", "Unstop", "Offline", "Space Technology", "₹1,00,000", 2, 5, 30, "Python,C++,Algorithms,Data Science", "ECE,EEE,CSE,MECH"),
    ]

    for i, d in enumerate(hackathons_data):
        title, org, platform, mode, theme, prize, min_team, max_team, days_from_now, tags, depts = d
        reg_dl = date.today() + timedelta(days=days_from_now)
        h = Hackathon(
            title=title, organizer=org, platform=platform, mode=mode, theme=theme,
            description=f"A {theme} hackathon organized by {org}. Top teams win exciting prizes.",
            prize_pool=prize, team_size_min=min_team, team_size_max=max_team,
            registration_deadline=reg_dl,
            event_start_date=reg_dl + timedelta(days=15),
            event_end_date=reg_dl + timedelta(days=17),
            registration_link=f"https://{platform.lower()}.io/hackathon/{title.lower().replace(' ','-')[:30]}",
            eligible_departments=depts,
            skill_tags=tags
        )
        db.add(h)

    db.flush()

    # Some student registrations
    hackathons = db.query(Hackathon).all()
    students = db.query(Student).limit(100).all()
    for student in random.sample(students, 40):
        h = random.choice(hackathons)
        existing = db.query(HackathonRegistration).filter(
            HackathonRegistration.student_id == student.id,
            HackathonRegistration.hackathon_id == h.id
        ).first()
        if not existing:
            reg = HackathonRegistration(
                student_id=student.id, hackathon_id=h.id,
                team_name=f"Team {fake.word().capitalize()}{random.randint(10,99)}",
                result=random.choice([None, None, None, "Participant", "Runner-up"])
            )
            db.add(reg)

    db.commit()
    print(f"   ✅ {len(hackathons_data)} hackathons seeded.")

# ════════════════════════════════════════════════════════════════
#  AGENT 9 — TRANSPORT
# ════════════════════════════════════════════════════════════════
def seed_transport(db: Session):
    if db.query(Bus).count() > 0:
        print("⏭️  Transport data already seeded. Skipping.")
        return

    print("🚌 Seeding Transport data...")

    bus_routes = [
        ("BUS-01", "City Center → Campus", ["City Bus Stand", "Railway Station", "Market Road", "Anna Nagar", "Tech Park", "College Main Gate"], "06:30", "07:45"),
        ("BUS-02", "North City → Campus", ["Airport Road", "Phase II", "Coimbatore North", "Gandhipuram", "Town Hall", "College Main Gate"], "07:00", "08:15"),
        ("BUS-03", "South Suburb → Campus", ["Singanallur", "Ganapathy", "Saravanampatti", "Peelamedu", "Avinashi Road", "College Main Gate"], "06:45", "08:00"),
        ("BUS-04", "Campus Shuttle A", ["College Main Gate", "Boys Hostel A", "Boys Hostel B", "Girls Hostel A", "CS Block"], "07:30", "07:50"),
        ("BUS-05", "Campus Shuttle B", ["College Main Gate", "Admin Block", "Library", "Cafeteria", "EC Block", "Sports Complex"], "08:00", "08:20"),
    ]

    for bus_num, route_name, stops, dep, arr in bus_routes:
        bus = Bus(
            bus_number=bus_num, route_name=route_name, capacity=50,
            driver_name=fake.name(), driver_phone=f"9{random.randint(100000000,999999999)}",
            is_active=True
        )
        db.add(bus)
        db.flush()

        # Add stops
        for i, stop_name in enumerate(stops):
            dep_h, dep_m = map(int, dep.split(':'))
            min_offset = i * 10
            arr_h = dep_h + (dep_m + min_offset) // 60
            arr_m = (dep_m + min_offset) % 60
            bs = BusStop(
                bus_id=bus.id, stop_name=stop_name, stop_order=i + 1,
                scheduled_arrival=f"{arr_h:02d}:{arr_m:02d}",
                latitude=11.0160 + i * 0.002 + random.uniform(-0.001, 0.001),
                longitude=76.9556 + i * 0.002 + random.uniform(-0.001, 0.001)
            )
            db.add(bs)

        # Schedules
        for direction, dep_t, arr_t in [("To Campus", dep, arr), ("From Campus", arr, dep)]:
            sched = BusSchedule(
                bus_id=bus.id, direction=direction, departure_time=dep_t,
                arrival_time=arr_t, days_of_operation="Mon-Fri"
            )
            db.add(sched)

        # Historical delay data
        for day_offset in range(60):
            delay_min = max(0, int(random.gauss(5, 8)))
            delay = BusDelay(
                bus_id=bus.id,
                delay_date=date.today() - timedelta(days=day_offset),
                delay_minutes=delay_min,
                reason=random.choice(["Traffic", "Traffic", "Traffic", "Breakdown", "Weather", None])
            )
            db.add(delay)

    db.commit()
    print(f"   ✅ {len(bus_routes)} buses with stops, schedules, and 60-day delay history seeded.")

# ════════════════════════════════════════════════════════════════
#  AGENT 10 — FEEDBACK
# ════════════════════════════════════════════════════════════════
def seed_feedback(db: Session):
    if db.query(FeedbackForm).count() > 0:
        print("⏭️  Feedback data already seeded. Skipping.")
        return

    print("📝 Seeding Feedback data...")

    forms = [
        FeedbackForm(title="Faculty Teaching Quality", target_type="Faculty", is_active=True),
        FeedbackForm(title="Course Content & Relevance", target_type="Course", is_active=True),
        FeedbackForm(title="Hostel Facilities", target_type="Hostel", is_active=True),
        FeedbackForm(title="Cafeteria Quality", target_type="Cafeteria", is_active=True),
        FeedbackForm(title="Campus General Feedback", target_type="General", is_active=True),
    ]
    for f in forms:
        db.add(f)
    db.flush()

    students = db.query(Student).limit(200).all()
    faculty_list = db.query(Faculty).all()
    courses = db.query(Course).limit(20).all()

    feedback_texts_positive = [
        "Excellent teaching! Very clear explanations.",
        "The professor made complex topics easy to understand.",
        "Best course I've taken this semester!",
        "Very interactive and engaging lectures.",
        "Always available for doubts and very helpful.",
    ]
    feedback_texts_negative = [
        "Lectures are too fast and hard to follow.",
        "The course content seems outdated.",
        "Not enough practical sessions.",
        "Could improve the teaching methodology.",
        "Attendance marking is very strict and unfair.",
    ]
    feedback_texts_neutral = [
        "Average experience, nothing exceptional.",
        "Okay course, could have more examples.",
        "The content is fine but delivery needs work.",
        "Mixed feelings about this course.",
        "Some topics were good, some were rushed.",
    ]

    responses_added = 0
    for student in students:
        # Faculty feedback
        for _ in range(random.randint(1, 4)):
            faculty = random.choice(faculty_list)
            rating = round(random.gauss(3.8, 0.9), 1)
            rating = max(1.0, min(5.0, rating))
            if rating >= 4.0:
                text = random.choice(feedback_texts_positive)
            elif rating <= 2.5:
                text = random.choice(feedback_texts_negative)
            else:
                text = random.choice(feedback_texts_neutral)

            from app.agents.feedback_agent import _analyze_sentiment
            sent_label, sent_score = _analyze_sentiment(text)

            resp = FeedbackResponse(
                form_id=forms[0].id, student_id=student.id,
                faculty_id=faculty.id, rating=rating,
                feedback_text=text, sentiment=sent_label, sentiment_score=sent_score
            )
            db.add(resp)
            responses_added += 1

    db.commit()
    print(f"   ✅ {len(forms)} forms, {responses_added} feedback responses seeded.")

# ════════════════════════════════════════════════════════════════
#  AGENT 11 — ALUMNI
# ════════════════════════════════════════════════════════════════
def seed_alumni(db: Session):
    if db.query(Alumni).count() > 0:
        print("⏭️  Alumni data already seeded. Skipping.")
        return

    print("🤝 Seeding Alumni data...")

    companies_list = [
        "Google", "Microsoft", "Amazon", "Meta", "Apple", "Goldman Sachs",
        "JP Morgan", "Infosys", "TCS", "Wipro", "Zoho", "Freshworks",
        "Samsung", "ISRO", "L&T", "Deloitte", "McKinsey", "Tesla",
        "NVIDIA", "Adobe", "Flipkart", "Swiggy", "Razorpay", "CRED"
    ]
    roles = [
        "Software Engineer", "Senior Software Engineer", "Data Scientist",
        "ML Engineer", "Backend Developer", "Full Stack Developer",
        "Product Manager", "DevOps Engineer", "Research Scientist",
        "System Architect", "Technical Lead", "Engineering Manager",
        "Data Analyst", "Frontend Developer", "Embedded Systems Engineer"
    ]
    industries = ["Technology", "Finance", "Research", "Consulting", "E-Commerce", "Government"]
    expertise = [
        "ML,Backend,Python", "Frontend,React,JavaScript", "Data Science,AI,Python",
        "DevOps,Cloud,AWS", "Embedded,IoT,C++", "Finance,Quant,Python",
        "Startup,Product,Growth", "Research,NLP,Deep Learning", "Backend,Java,System Design"
    ]

    skills = db.query(Skill).all()
    if not skills:
        print("   ⚠️  No skills found. Run placement seed first.")
        return

    alumni_list = []
    for i in range(1, 101):  # 100 alumni
        dept = random.choice(DEPARTMENTS)
        grad_year = random.randint(2015, 2024)
        exp = 2026 - grad_year
        a = Alumni(
            alumni_id=f"AL{10000+i}",
            name=fake.name(),
            department=dept,
            graduation_year=grad_year,
            current_company=random.choice(companies_list),
            current_role=random.choice(roles),
            industry=random.choice(industries),
            experience_years=exp,
            location=random.choice(["Bengaluru", "Hyderabad", "Chennai", "Mumbai", "Pune", "Delhi", "Coimbatore"]),
            linkedin_url=f"https://linkedin.com/in/{fake.user_name()}",
            email=fake.email(),
            is_mentor=random.random() > 0.25,
            bio=f"Passionate {random.choice(roles)} with {exp}+ years of experience at top companies.",
            expertise_areas=random.choice(expertise)
        )
        db.add(a)
        alumni_list.append(a)

    db.flush()

    # Alumni skills
    for alumni in alumni_list:
        n_skills = random.randint(3, 8)
        for skill in random.sample(skills, n_skills):
            db.add(AlumniSkill(alumni_id=alumni.id, skill_id=skill.id))

    db.commit()
    print(f"   ✅ {len(alumni_list)} alumni with skills seeded.")

# ════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════
def main():
    print("=" * 60)
    print("  Smart Campus — Master Seed Script (11 Agents)")
    print("=" * 60)

    create_tables()
    db = SessionLocal()

    try:
        seed_navigation(db)
        seed_hostel(db)
        seed_cafeteria(db)
        seed_placement(db)
        seed_exam(db)
        seed_hackathon(db)
        seed_transport(db)
        seed_feedback(db)
        seed_alumni(db)
    finally:
        db.close()

    print("\n" + "=" * 60)
    print("  ✅ ALL AGENTS SEEDED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
