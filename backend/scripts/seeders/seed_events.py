from sqlalchemy.orm import Session
from app.models.models import (
    Company, Skill, CompanySkillRequirement, PlacementProfile, StudentSkill,
    Hackathon, HackathonRegistration, ExamSchedule, HallTicket, ExamResult,
    Alumni, AlumniSkill, MentorshipRequest, Event, Student, Course
)
import random
from datetime import date, timedelta
import json

def seed_events(db: Session):
    print("Seeding Skills...")
    skills = [
        "Python", "React", "Node.js", "Java", "SQL", "C++", 
        "Machine Learning", "Data Structures", "Cloud Computing",
        "AWS", "Docker", "Kubernetes", "UI/UX Design", "Communication", "Leadership"
    ]
    db_skills = []
    for s in skills:
        skill = Skill(name=s, category="Programming" if s not in ["Communication", "Leadership"] else "Soft")
        db.add(skill)
        db_skills.append(skill)
    db.commit()

    print("Seeding Companies (500)...")
    roles = ["Software Engineer", "Data Scientist", "Product Manager", "DevOps Engineer", "Frontend Developer", "Backend Developer"]
    industries = ["IT", "Finance", "Healthcare", "EdTech", "E-commerce"]
    depts = ["CSE,IT", "CSE,IT,ECE", "MECH,CIVIL", "MBA", "ALL"]
    
    db_companies = []
    for i in range(1, 501):
        c = Company(
            name=f"Company {i} {random.choice(['Tech', 'Solutions', 'Labs', 'Systems'])}",
            industry=random.choice(industries),
            package_lpa_min=round(random.uniform(3.5, 10.0), 1),
            package_lpa_max=round(random.uniform(10.0, 40.0), 1),
            min_cgpa=random.choice([6.0, 7.0, 7.5, 8.0]),
            eligible_departments=random.choice(depts),
            job_role=random.choice(roles),
            interview_rounds=random.randint(2, 5),
            description=f"A leading {random.choice(industries)} company hiring talented graduates.",
            website=f"https://company{i}.com",
            visit_date=date(2026, 8, 1) + timedelta(days=random.randint(0, 90))
        )
        db.add(c)
        db_companies.append(c)
    db.commit()

    print("Seeding Company Skill Requirements...")
    reqs = []
    for c in db_companies:
        req_skills = random.sample(db_skills, random.randint(2, 4))
        for sk in req_skills:
            reqs.append(CompanySkillRequirement(
                company_id=c.id,
                skill_id=sk.id,
                importance=random.choice(["Required", "Preferred"])
            ))
    db.bulk_save_objects(reqs)
    db.commit()

    print("Seeding Placement Profiles...")
    students = db.query(Student).all()
    profiles = []
    student_skills = []
    for s in students:
        # 60% of students have profiles + S100001
        if random.random() < 0.6 or s.student_id == "S100001":
            profiles.append(PlacementProfile(
                student_id=s.id,
                resume_score=round(random.uniform(50, 95), 1),
                readiness_score=round(random.uniform(50, 95), 1),
                coding_score=round(random.uniform(50, 95), 1),
                communication_score=round(random.uniform(50, 95), 1),
                ai_score=round(random.uniform(50, 95), 1),
                db_score=round(random.uniform(50, 95), 1),
                mock_interviews_done=random.randint(0, 5),
                internships=random.randint(0, 3),
                projects=random.randint(1, 5),
                certifications=random.randint(0, 4),
                linkedin_url=f"https://linkedin.com/in/stu{s.id}",
                github_url=f"https://github.com/stu{s.id}"
            ))
            s_skills = random.sample(db_skills, random.randint(2, 6))
            for sk in s_skills:
                student_skills.append(StudentSkill(
                    student_id=s.id,
                    skill_id=sk.id,
                    proficiency=random.choice(["Beginner", "Intermediate", "Advanced"])
                ))
    db.bulk_save_objects(profiles)
    db.bulk_save_objects(student_skills)
    db.commit()

    print("Seeding Hackathons (300)...")
    hack_orgs = ["Devfolio", "Unstop", "MLH", "Smart India Hackathon", "Internal College", "Company Challenge"]
    hacks = []
    for i in range(1, 301):
        hacks.append(Hackathon(
            title=f"Hackathon {i} 2026",
            organizer=random.choice(hack_orgs),
            platform=random.choice(["Devfolio", "Unstop", "HackerEarth", "Offline"]),
            mode=random.choice(["Online", "Offline", "Hybrid"]),
            theme=random.choice(["Web3", "AI/ML", "Healthcare", "FinTech", "EdTech"]),
            prize_pool=f"₹{random.randint(1, 50)} Lakhs",
            team_size_min=random.randint(1, 2),
            team_size_max=random.randint(3, 6),
            registration_deadline=date(2026, 8, 1) + timedelta(days=random.randint(10, 60)),
            event_start_date=date(2026, 8, 1) + timedelta(days=random.randint(65, 80)),
            event_end_date=date(2026, 8, 1) + timedelta(days=random.randint(81, 85))
        ))
    db.bulk_save_objects(hacks)
    db.commit()

    print("Seeding Exams...")
    courses = db.query(Course).all()
    exams = []
    for c in courses:
        exams.append(ExamSchedule(
            course_id=c.id,
            exam_type=random.choice(["Internal 1", "Internal 2", "Semester"]),
            exam_date=date(2026, 11, 15) + timedelta(days=random.randint(0, 30)),
            start_time="09:00",
            end_time="12:00",
            venue=f"Block {random.choice(['A', 'B', 'C'])}",
            max_marks=100,
            semester=c.semester,
            academic_year=2026
        ))
    db.bulk_save_objects(exams)
    db.commit()

    print("Seeding Alumni (1500)...")
    alumni_list = []
    for i in range(1, 1501):
        alumni_list.append(Alumni(
            alumni_id=f"AL{i:04d}",
            name=f"Alumni Name {i}",
            department=random.choice(["CSE", "IT", "MECH", "ECE"]),
            graduation_year=random.randint(2010, 2025),
            current_company=random.choice(["Google", "Microsoft", "TCS", "Infosys", "Amazon"]),
            current_role=random.choice(roles),
            industry="IT",
            experience_years=random.randint(1, 15),
            linkedin_url=f"https://linkedin.com/in/alumni{i}"
        ))
    db.bulk_save_objects(alumni_list)
    db.commit()

    print("Seeding Events (200)...")
    events = []
    for i in range(1, 201):
        events.append(Event(
            event_name=f"University Event {i}",
            event_type=random.choice(["Cultural", "Technical", "Sports", "Seminar"]),
            date=date(2026, 8, 1) + timedelta(days=random.randint(0, 300)),
            venue="Main Auditorium",
            organizer="Student Council"
        ))
    db.bulk_save_objects(events)
    db.commit()
