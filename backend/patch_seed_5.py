from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.models import (
    Student, HostelAllocation, HostelRoom, 
    Building, CampusRoute, 
    FoodItem, CafeteriaMenu, 
    PlacementProfile, Skill, StudentSkill
)
import random
import json
from datetime import date

db = SessionLocal()

print("1. Fixing Hostel Allocations for Quick Access Users...")
quick_users = ['S100001', 'S100025', 'S100100', 'S100200', 'S100500']
students = db.query(Student).filter(Student.student_id.in_(quick_users)).all()
rooms = db.query(HostelRoom).limit(10).all()

for i, s in enumerate(students):
    alloc = db.query(HostelAllocation).filter_by(student_id=s.id).first()
    if not alloc and i < len(rooms):
        db.add(HostelAllocation(student_id=s.id, room_id=rooms[i].id, check_in_date=date(2025, 8, 1), is_active=True))
db.commit()

print("2. Generating Campus Routes for Navigation...")
buildings = db.query(Building).all()
if buildings:
    for _ in range(100):
        b1 = random.choice(buildings)
        b2 = random.choice(buildings)
        if b1.id != b2.id:
            exists = db.query(CampusRoute).filter_by(source_id=b1.id, destination_id=b2.id).first()
            if not exists:
                dist = random.uniform(50.0, 500.0)
                time = dist / 80.0
                db.add(CampusRoute(
                    source_id=b1.id, 
                    destination_id=b2.id, 
                    distance_meters=round(dist, 2), 
                    walk_time_minutes=round(time, 1),
                    path_description=f"Path from {b1.name} to {b2.name}"
                ))
    db.commit()

print("3. Generating Cafeteria Menu...")
food_items = db.query(FoodItem).all()
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
slots = ["Breakfast", "Lunch", "Snacks", "Dinner"]
if food_items:
    for day in days:
        for slot in slots:
            selected_items = random.sample(food_items, min(5, len(food_items)))
            for item in selected_items:
                exists = db.query(CafeteriaMenu).filter_by(food_item_id=item.id, day_of_week=day, meal_slot=slot).first()
                if not exists:
                    db.add(CafeteriaMenu(
                        food_item_id=item.id,
                        day_of_week=day,
                        meal_slot=slot,
                        is_available=True
                    ))
    db.commit()

print("4. Generating Placement Profiles and Skills...")
skills_list = ["Python", "React", "Node.js", "Java", "SQL", "C++", "Machine Learning", "Data Structures"]
db_skills = []
for s_name in skills_list:
    sk = db.query(Skill).filter_by(name=s_name).first()
    if not sk:
        sk = Skill(name=s_name, category="Programming")
        db.add(sk)
    db_skills.append(sk)
db.commit()
db_skills = db.query(Skill).all()

all_students = db.query(Student).all()
profiles = []
student_skills = []

for s in all_students:
    if random.random() < 0.5 or s.student_id == "S100001":
        # Check if profile exists
        existing_profile = db.query(PlacementProfile).filter_by(student_id=s.id).first()
        if not existing_profile:
            profiles.append(PlacementProfile(
                student_id=s.id,
                resume_score=round(random.uniform(50, 95), 1),
                readiness_score=round(random.uniform(50, 95), 1),
                mock_interviews_done=random.randint(0, 5),
                internships=random.randint(0, 2),
                projects=random.randint(1, 5),
                certifications=random.randint(0, 3),
                linkedin_url=f"https://linkedin.com/in/stu{s.id}",
                github_url=f"https://github.com/stu{s.id}"
            ))
            
            # Add skills
            chosen_skills = random.sample(db_skills, random.randint(2, 5))
            for sk in chosen_skills:
                student_skills.append(StudentSkill(
                    student_id=s.id,
                    skill_id=sk.id,
                    proficiency=random.choice(["Beginner", "Intermediate", "Advanced"])
                ))

if profiles:
    db.bulk_save_objects(profiles)
if student_skills:
    db.bulk_save_objects(student_skills)
db.commit()

print("Successfully applied supplemental seed data!")
