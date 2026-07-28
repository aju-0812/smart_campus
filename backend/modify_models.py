import re

file_path = "app/models/models.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Modify Student
student_addition = """    register_number = Column(String, unique=True, nullable=True)
    roll_number = Column(String, unique=True, nullable=True)
    dob = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    section = Column(String, default="A")
    address = Column(Text, nullable=True)
    parent_details = Column(Text, nullable=True)
    is_hosteller = Column(Boolean, default=False)
    advisor_id = Column(Integer, ForeignKey("faculty.id"), nullable=True)
    attendance_percentage = Column(Float, default=0.0)
    at_risk_flag = Column(Boolean, default=False)
    prediction_data = Column(JSON, nullable=True)"""
content = re.sub(r'(class Student\(Base\):.*?    password = Column\(String, nullable=False, default="pass123"\))', r'\1\n' + student_addition, content, flags=re.DOTALL)

# 2. Modify Faculty
faculty_addition = """    gender = Column(String, nullable=True)
    age = Column(Integer, nullable=True)"""
content = re.sub(r'(class Faculty\(Base\):.*?    faculty_name = Column\(String, nullable=False\))', r'\1\n' + faculty_addition, content, flags=re.DOTALL)

# 3. Modify Course
course_addition = """    is_theory = Column(Boolean, default=True)
    is_practical = Column(Boolean, default=False)
    is_lab = Column(Boolean, default=False)
    is_project = Column(Boolean, default=False)"""
content = re.sub(r'(class Course\(Base\):.*?    type = Column\(String, default="Core"\))', r'\1\n' + course_addition, content, flags=re.DOTALL)

# 4. Modify TimetableSlot
content = re.sub(r'course_id = Column\(Integer, ForeignKey\("courses.id"\), nullable=False\)', 'course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)', content)
timetable_addition = """    slot_type = Column(String, default="Lecture")  # Lecture, Lab, Tea Break, Lunch Break, Library Hour, Seminar Hour"""
content = re.sub(r'(class TimetableSlot\(Base\):.*?    section = Column\(String, nullable=False, default="A"\))', r'\1\n' + timetable_addition, content, flags=re.DOTALL)

# 5. Modify Classroom
classroom_addition = """    has_smartboard = Column(Boolean, default=True)
    has_projector = Column(Boolean, default=True)
    is_lab = Column(Boolean, default=False)
    floor = Column(Integer, default=1)"""
content = re.sub(r'(class Classroom\(Base\):.*?    capacity = Column\(Integer, nullable=False\))', r'\1\n' + classroom_addition, content, flags=re.DOTALL)

# 6. Modify Company
company_addition = """    drive_date = Column(Date, nullable=True)
    job_role = Column(String, nullable=True)
    selection_process = Column(Text, nullable=True)"""
content = re.sub(r'(class Company\(Base\):.*?    average_package = Column\(Float, nullable=True\))', r'\1\n' + company_addition, content, flags=re.DOTALL)

# 7. Modify Hackathon
hackathon_addition = """    organizer = Column(String, nullable=True)
    venue = Column(String, nullable=True)
    registration_link = Column(String, nullable=True)"""
content = re.sub(r'(class Hackathon\(Base\):.*?    max_team_size = Column\(Integer, default=4\))', r'\1\n' + hackathon_addition, content, flags=re.DOTALL)

# 8. Modify Alumni
alumni_addition = """    mentoring_areas = Column(String, nullable=True)"""
content = re.sub(r'(class Alumni\(Base\):.*?    current_location = Column\(String, nullable=True\))', r'\1\n' + alumni_addition, content, flags=re.DOTALL)

# 9. Modify FeedbackResponse
feedback_addition = """    faculty_rating = Column(Integer, nullable=True)
    course_rating = Column(Integer, nullable=True)
    hostel_rating = Column(Integer, nullable=True)
    food_rating = Column(Integer, nullable=True)
    transport_rating = Column(Integer, nullable=True)"""
content = re.sub(r'(class FeedbackResponse\(Base\):.*?    overall_sentiment = Column\(String, nullable=True\))', r'\1\n' + feedback_addition, content, flags=re.DOTALL)

# 10. Modify MessMenu
mess_addition = """    calories = Column(Integer, nullable=True)
    protein_g = Column(Float, nullable=True)
    is_veg = Column(Boolean, default=True)
    healthy_rating = Column(Float, nullable=True)"""
content = re.sub(r'(class MessMenu\(Base\):.*?    item_name = Column\(String, nullable=False\))', r'\1\n' + mess_addition, content, flags=re.DOTALL)

# 11. Add New Models
new_models = """

# ════════════════════════════════════════════════════════════════
#  NEW MODELS (University, Lab, Book, Event, FAQ)
# ════════════════════════════════════════════════════════════════

class University(Base):
    __tablename__ = "university"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    campus_address = Column(String, nullable=False)
    website = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    vision = Column(Text, nullable=True)
    mission = Column(Text, nullable=True)
    principal = Column(String, nullable=True)
    vice_principal = Column(String, nullable=True)
    dean_academics = Column(String, nullable=True)
    dean_students = Column(String, nullable=True)
    registrar = Column(String, nullable=True)
    working_hours = Column(String, nullable=True)
    campus_map_url = Column(String, nullable=True)

class Lab(Base):
    __tablename__ = "labs"
    id = Column(Integer, primary_key=True, index=True)
    lab_name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    building = Column(String, nullable=True)
    room_number = Column(String, nullable=True)
    capacity = Column(Integer, default=30)
    equipment_list = Column(Text, nullable=True)
    lab_assistant = Column(String, nullable=True)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    rack_number = Column(String, nullable=True)
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, nullable=False)
    event_type = Column(String, nullable=False) # Technical, Cultural, Sports, Workshop, Guest Lecture
    date = Column(Date, nullable=False)
    venue = Column(String, nullable=True)
    organizer = Column(String, nullable=True)

class FAQ(Base):
    __tablename__ = "faqs"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String, nullable=True)
"""

content += new_models

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("models.py modified successfully!")
