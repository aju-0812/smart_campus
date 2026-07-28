import re

file_path = "scripts/seed_db.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Placement block
old_placement = """        # 9. PLACEMENT (100)
        print("Seeding Placement (100 Companies)...")
        comp_list = []
        for i in range(100):
            comp_list.append({
                "company_name": fake.company(),
                "industry": "IT",
                "average_package": random.uniform(3.5, 25.0),
                "drive_date": date(2026, 5, random.randint(1, 30)),
                "job_role": random.choice(["Software Engineer", "Analyst", "Consultant"]),
                "selection_process": "Aptitude -> Coding -> Interview"
            })
        chunk_insert(db, Company, comp_list)"""

new_placement = """        # 9. PLACEMENT (100)
        print("Seeding Placement (100 Companies)...")
        comp_list = []
        for i in range(100):
            p_min = random.uniform(3.5, 10.0)
            comp_list.append({
                "name": fake.company(),
                "industry": random.choice(["IT", "Finance", "Consulting", "Core"]),
                "package_lpa_min": round(p_min, 1),
                "package_lpa_max": round(p_min + random.uniform(1.0, 5.0), 1),
                "min_cgpa": round(random.uniform(6.0, 8.5), 1),
                "eligible_departments": "CSE,ECE,IT",
                "description": "Leading global company.",
                "drive_date": date(2026, 5, random.randint(1, 30)),
                "job_role": random.choice(["Software Engineer", "Analyst", "Consultant"]),
                "selection_process": "Aptitude -> Coding -> Interview"
            })
        chunk_insert(db, Company, comp_list)"""
content = content.replace(old_placement, new_placement)

# Replace Exam block
old_exam = """        # 13. EXAMS
        print("Seeding Exams...")
        exam_list = []
        for cid in course_pk[:100]:
            exam_list.append({"exam_name": "Semester Exam", "course_id": cid, "exam_date": date(2026, 6, 1), "start_time": "10:00", "end_time": "13:00", "venue": "Main Hall", "total_marks": 100})
        chunk_insert(db, ExamSchedule, exam_list)"""

new_exam = """        # 13. EXAMS
        print("Seeding Exams...")
        exam_list = []
        for c in all_courses[:100]:
            exam_list.append({"exam_type": "Semester Exam", "course_id": c.id, "exam_date": date(2026, 6, 1), "start_time": "10:00", "end_time": "13:00", "venue": "Main Hall", "max_marks": 100, "semester": c.semester})
        chunk_insert(db, ExamSchedule, exam_list)"""
content = content.replace(old_exam, new_exam)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Patched seed_db.py successfully!")
