import re

file_path = "scripts/seed_db.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Alumni block
old_alumni = """        alumni_list = []
        for i in range(1000):
            alumni_list.append({"student_id": random.choice(all_students).id, "graduation_year": 2024, "current_company": fake.company(), "mentoring_areas": "AI, ML, Career"})
        chunk_insert(db, Alumni, alumni_list)"""

new_alumni = """        alumni_list = []
        for i in range(1000):
            alumni_list.append({"alumni_id": f"AL{i}", "name": fake.name(), "department": "Computer Science", "graduation_year": 2024, "current_company": fake.company(), "mentoring_areas": "AI, ML, Career"})
        chunk_insert(db, Alumni, alumni_list)"""
content = content.replace(old_alumni, new_alumni)

# Replace Feedback block
old_fb = """        fb_list = []
        for i in range(5000):
            fb_list.append({"form_id": 1, "student_id": random.choice(all_students).id, "faculty_rating": 4, "course_rating": 5, "hostel_rating": 3, "food_rating": 4, "transport_rating": 5, "overall_sentiment": "Positive"})
        chunk_insert(db, FeedbackResponse, fb_list)"""

new_fb = """        db.add(FeedbackForm(title="Course Feedback", target_type="Course"))
        db.commit()
        fb_list = []
        for i in range(5000):
            fb_list.append({"form_id": 1, "student_id": random.choice(all_students).id, "rating": 4.5, "faculty_rating": 4, "course_rating": 5, "hostel_rating": 3, "food_rating": 4, "transport_rating": 5, "overall_sentiment": "Positive"})
        chunk_insert(db, FeedbackResponse, fb_list)"""
content = content.replace(old_fb, new_fb)

# Need to import FeedbackForm at the top if not imported
if "FeedbackForm" not in content:
    content = content.replace("FAQ", "FAQ, FeedbackForm")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Patched seed_db.py Alumni and Feedback successfully!")
