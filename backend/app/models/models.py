from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, Date, Time,
    Boolean, UniqueConstraint, Text, DateTime, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

# ════════════════════════════════════════════════════════════════
#  EXISTING MODELS (Timetable + Attendance agents)
# ════════════════════════════════════════════════════════════════

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(String, unique=True, index=True, nullable=False)
    department_name = Column(String, nullable=False)
    department_code = Column(String, nullable=False)
    hod_id = Column(Integer, ForeignKey("faculty.id", use_alter=True), nullable=True)
    building = Column(String, nullable=True)
    floor = Column(Integer, nullable=True)
    office_phone = Column(String, nullable=True)
    office_email = Column(String, nullable=True)
    description = Column(Text, nullable=True)

    courses = relationship("Course", back_populates="department")
    faculty = relationship("Faculty", foreign_keys="[Faculty.department_id]", back_populates="department_ref")


class ConversationSession(Base):
    __tablename__ = "conversation_sessions"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    last_agent = Column(String, nullable=True)
    last_entity = Column(String, nullable=True)
    last_department = Column(String, nullable=True)
    last_faculty = Column(String, nullable=True)
    last_course = Column(String, nullable=True)
    last_day = Column(String, nullable=True)
    last_subject = Column(String, nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    department = Column(String, nullable=False)
    semester = Column(Integer, nullable=False)
    cgpa = Column(Float, default=7.0)
    phone = Column(String, nullable=True)
    year_of_joining = Column(Integer, default=2022)
    password = Column(String, nullable=False, default="pass123")
    register_number = Column(String, unique=True, nullable=True)
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
    prediction_data = Column(JSON, nullable=True)

    attendance = relationship("AttendanceRecord", back_populates="student")
    hostel_allocation = relationship("HostelAllocation", back_populates="student", uselist=False)
    food_orders = relationship("FoodOrder", back_populates="student")
    food_ratings = relationship("FoodRating", back_populates="student")
    placement_profile = relationship("PlacementProfile", back_populates="student", uselist=False)
    hackathon_registrations = relationship("HackathonRegistration", back_populates="student")
    feedback_responses = relationship("FeedbackResponse", back_populates="student")
    mentorship_requests = relationship("MentorshipRequest", back_populates="student")


class Faculty(Base):
    __tablename__ = "faculty"
    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(String, unique=True, index=True, nullable=False)
    faculty_name = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    designation = Column(String, nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    qualification = Column(String, nullable=True)
    highest_degree = Column(String, nullable=True)
    specialization = Column(String, nullable=True)
    experience_years = Column(Integer, default=5)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    office_room = Column(String, nullable=True)
    building = Column(String, nullable=True)
    office_hours = Column(String, nullable=True)
    research_areas = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    google_scholar = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    is_hod = Column(Boolean, default=False)
    is_dean = Column(Boolean, default=False)
    office_building = Column(String, nullable=True)
    office_hours = Column(String, nullable=True)
    subjects = Column(String, nullable=True)
    research_area = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    google_scholar = Column(String, nullable=True)
    image_path = Column(String, nullable=True)
    is_hod = Column(Boolean, default=False)
    is_dean = Column(Boolean, default=False)

    department_ref = relationship("Department", foreign_keys=[department_id], back_populates="faculty")
    courses = relationship("Course", back_populates="faculty")
    timetable_slots = relationship("TimetableSlot", back_populates="faculty")
    feedback_responses = relationship("FeedbackResponse", back_populates="faculty")

    @property
    def name(self):
        return self.faculty_name


class Classroom(Base):
    __tablename__ = "classrooms"
    id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String, unique=True, index=True, nullable=False)
    building = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    has_smartboard = Column(Boolean, default=True)
    has_projector = Column(Boolean, default=True)
    is_lab = Column(Boolean, default=False)
    floor = Column(Integer, default=1)
    room_type = Column(String, default="Lecture Hall")

    timetable_slots = relationship("TimetableSlot", back_populates="classroom")


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(String, unique=True, index=True, nullable=False)
    course_name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    semester = Column(Integer, nullable=False)
    credits = Column(Integer, default=3)
    faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=False)
    type = Column(String, default="Core")
    is_theory = Column(Boolean, default=True)
    is_practical = Column(Boolean, default=False)
    is_lab = Column(Boolean, default=False)
    is_project = Column(Boolean, default=False)

    department = relationship("Department", back_populates="courses")
    faculty = relationship("Faculty", back_populates="courses")
    timetable_slots = relationship("TimetableSlot", back_populates="course")
    attendance_records = relationship("AttendanceRecord", back_populates="course")
    exam_schedules = relationship("ExamSchedule", back_populates="course")
    feedback_responses = relationship("FeedbackResponse", back_populates="course")

    @property
    def name(self):
        return self.course_name

    @property
    def course_code(self):
        return self.course_id


class TimetableSlot(Base):
    __tablename__ = "timetable_slots"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=False)
    day_of_week = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    semester = Column(Integer, nullable=False)
    academic_year = Column(Integer, nullable=False, default=2026)
    section = Column(String, nullable=False, default="A")
    slot_type = Column(String, default="Lecture")  # Lecture, Lab, Tea Break, Lunch Break, Library Hour, Seminar Hour
    period_number = Column(Integer, nullable=True)

    course = relationship("Course", back_populates="timetable_slots")
    classroom = relationship("Classroom", back_populates="timetable_slots")
    faculty = relationship("Faculty", back_populates="timetable_slots")

    __table_args__ = (
        UniqueConstraint('classroom_id', 'day_of_week', 'start_time', 'academic_year', name='_classroom_slot_uc'),
    )


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    date = Column(Date, nullable=False)
    status = Column(String, nullable=False)

    student = relationship("Student", back_populates="attendance")
    course = relationship("Course", back_populates="attendance_records")


# ════════════════════════════════════════════════════════════════
#  AGENT 3 — Campus Navigation
# ════════════════════════════════════════════════════════════════

class Building(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True, index=True)
    building_code = Column(String, unique=True, index=True, nullable=False)  # e.g. CSB, LIB
    name = Column(String, nullable=False)
    building_type = Column(String, nullable=False)  # academic/hostel/admin/sports/cafeteria
    floors = Column(Integer, default=1)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    description = Column(Text, nullable=True)

    routes_from = relationship("CampusRoute", foreign_keys="CampusRoute.source_id", back_populates="source_building")
    routes_to = relationship("CampusRoute", foreign_keys="CampusRoute.destination_id", back_populates="destination_building")


class CampusRoute(Base):
    __tablename__ = "campus_routes"
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)
    distance_meters = Column(Float, nullable=False)
    walk_time_minutes = Column(Float, nullable=False)
    path_description = Column(Text, nullable=True)
    is_accessible = Column(Boolean, default=True)  # wheelchair accessible

    source_building = relationship("Building", foreign_keys=[source_id], back_populates="routes_from")
    destination_building = relationship("Building", foreign_keys=[destination_id], back_populates="routes_to")


# ════════════════════════════════════════════════════════════════
#  AGENT 4 — Hostel Assistant
# ════════════════════════════════════════════════════════════════

class Hostel(Base):
    __tablename__ = "hostels"
    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)  # Male/Female
    total_rooms = Column(Integer, nullable=False)
    warden_name = Column(String, nullable=True)
    warden_phone = Column(String, nullable=True)

    rooms = relationship("HostelRoom", back_populates="hostel")


class HostelRoom(Base):
    __tablename__ = "hostel_rooms"
    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id"), nullable=False)
    room_number = Column(String, nullable=False)
    floor = Column(Integer, default=1)
    capacity = Column(Integer, default=2)
    room_type = Column(String, default="Double")  # Single/Double/Triple
    is_available = Column(Boolean, default=False)
    monthly_fee = Column(Float, default=3000.0)

    hostel = relationship("Hostel", back_populates="rooms")
    allocations = relationship("HostelAllocation", back_populates="room")


class HostelAllocation(Base):
    __tablename__ = "hostel_allocations"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("hostel_rooms.id"), nullable=False)
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)

    student = relationship("Student", back_populates="hostel_allocation")
    room = relationship("HostelRoom", back_populates="allocations")


class HostelComplaint(Base):
    __tablename__ = "hostel_complaints"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    complaint_text = Column(Text, nullable=False)
    category = Column(String, nullable=True)  # Electrical/Plumbing/Food/Cleanliness/Other
    status = Column(String, default="Open")  # Open/In Progress/Resolved
    priority = Column(String, default="Medium")  # Low/Medium/High
    created_at = Column(DateTime, server_default=func.now())
    resolved_at = Column(DateTime, nullable=True)

    student = relationship("Student")


class MessMenu(Base):
    __tablename__ = "mess_menu"
    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(String, nullable=False)
    meal_type = Column(String, nullable=False)  # Breakfast/Lunch/Snacks/Dinner
    items = Column(Text, nullable=False)  # comma-separated food items
    calories = Column(Integer, nullable=True)
    protein_g = Column(Float, nullable=True)
    is_veg = Column(Boolean, default=True)
    healthy_rating = Column(Float, nullable=True)
    calories_approx = Column(Integer, nullable=True)


# ════════════════════════════════════════════════════════════════
#  AGENT 5 — Cafeteria Recommendation
# ════════════════════════════════════════════════════════════════

class FoodItem(Base):
    __tablename__ = "food_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # Main/Snack/Beverage/Dessert
    cuisine = Column(String, nullable=False)  # Indian/Chinese/Continental/South Indian
    is_veg = Column(Boolean, default=True)
    price = Column(Float, nullable=False)
    calories = Column(Integer, nullable=True)
    protein_g = Column(Float, nullable=True)
    carbs_g = Column(Float, nullable=True)
    fat_g = Column(Float, nullable=True)
    avg_rating = Column(Float, default=3.5)
    tags = Column(String, nullable=True)  # spicy,healthy,quick

    orders = relationship("FoodOrder", back_populates="food_item")
    ratings = relationship("FoodRating", back_populates="food_item")


class CafeteriaMenu(Base):
    __tablename__ = "cafeteria_menu"
    id = Column(Integer, primary_key=True, index=True)
    food_item_id = Column(Integer, ForeignKey("food_items.id"), nullable=False)
    day_of_week = Column(String, nullable=False)
    meal_slot = Column(String, nullable=False)  # Breakfast/Lunch/Snacks/Dinner
    is_available = Column(Boolean, default=True)
    quantity_available = Column(Integer, default=50)

    food_item = relationship("FoodItem")


class FoodOrder(Base):
    __tablename__ = "food_orders"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    food_item_id = Column(Integer, ForeignKey("food_items.id"), nullable=False)
    order_date = Column(Date, nullable=False)
    quantity = Column(Integer, default=1)
    total_price = Column(Float, nullable=False)

    student = relationship("Student", back_populates="food_orders")
    food_item = relationship("FoodItem", back_populates="orders")


class FoodRating(Base):
    __tablename__ = "food_ratings"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    food_item_id = Column(Integer, ForeignKey("food_items.id"), nullable=False)
    rating = Column(Float, nullable=False)  # 1.0 to 5.0
    review = Column(Text, nullable=True)
    rated_at = Column(DateTime, server_default=func.now())

    student = relationship("Student", back_populates="food_ratings")
    food_item = relationship("FoodItem", back_populates="ratings")


# ════════════════════════════════════════════════════════════════
#  AGENT 6 — Placement Preparation
# ════════════════════════════════════════════════════════════════

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # Python, ML, SQL, React, etc.
    category = Column(String, nullable=False)  # Programming/Soft/Domain/Tool

    student_skills = relationship("StudentSkill", back_populates="skill")
    company_requirements = relationship("CompanySkillRequirement", back_populates="skill")
    alumni_skills = relationship("AlumniSkill", back_populates="skill")


class StudentSkill(Base):
    __tablename__ = "student_skills"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    proficiency = Column(String, default="Beginner")  # Beginner/Intermediate/Advanced

    student = relationship("Student")
    skill = relationship("Skill", back_populates="student_skills")


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    package_lpa_min = Column(Float, nullable=False)
    package_lpa_max = Column(Float, nullable=False)
    min_cgpa = Column(Float, default=6.0)
    eligible_departments = Column(String, nullable=False)  # comma-sep: CSE,ECE
    job_role = Column(String, nullable=False, default="Software Engineer")
    interview_rounds = Column(Integer, default=3)
    description = Column(Text, nullable=True)
    website = Column(String, nullable=True)
    visit_date = Column(Date, nullable=True)

    skill_requirements = relationship("CompanySkillRequirement", back_populates="company")


class CompanySkillRequirement(Base):
    __tablename__ = "company_skill_requirements"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    importance = Column(String, default="Required")  # Required/Preferred

    company = relationship("Company", back_populates="skill_requirements")
    skill = relationship("Skill", back_populates="company_requirements")


class PlacementProfile(Base):
    __tablename__ = "placement_profiles"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True, nullable=False)
    resume_score = Column(Float, default=0.0)  # 0-100
    readiness_score = Column(Float, default=0.0)  # 0-100
    coding_score = Column(Float, default=0.0)
    communication_score = Column(Float, default=0.0)
    ai_score = Column(Float, default=0.0)
    db_score = Column(Float, default=0.0)
    mock_interviews_done = Column(Integer, default=0)
    internships = Column(Integer, default=0)
    projects = Column(Integer, default=0)
    certifications = Column(Integer, default=0)
    linkedin_url = Column(String, nullable=True)
    github_url = Column(String, nullable=True)

    student = relationship("Student", back_populates="placement_profile")


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)  # DSA/OS/DBMS/CN/HR/Python/ML
    difficulty = Column(String, default="Medium")  # Easy/Medium/Hard
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    company_type = Column(String, nullable=True)  # Product/Service/Startup


# ════════════════════════════════════════════════════════════════
#  AGENT 7 — Exam Discovery
# ════════════════════════════════════════════════════════════════

class ExamSchedule(Base):
    __tablename__ = "exam_schedules"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    exam_type = Column(String, nullable=False)  # Internal1/Internal2/EndSem/Supplementary
    exam_date = Column(Date, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    venue = Column(String, nullable=False)
    semester = Column(Integer, nullable=False)
    academic_year = Column(Integer, default=2026)
    max_marks = Column(Integer, default=100)

    course = relationship("Course", back_populates="exam_schedules")
    hall_tickets = relationship("HallTicket", back_populates="exam")


class HallTicket(Base):
    __tablename__ = "hall_tickets"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exam_schedules.id"), nullable=False)
    seat_number = Column(String, nullable=False)
    is_issued = Column(Boolean, default=True)

    student = relationship("Student")
    exam = relationship("ExamSchedule", back_populates="hall_tickets")


class ExamResult(Base):
    __tablename__ = "exam_results"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exam_schedules.id"), nullable=False)
    marks_obtained = Column(Float, nullable=False)
    grade = Column(String, nullable=True)  # O/A+/A/B+/B/C/F
    is_pass = Column(Boolean, default=True)

    student = relationship("Student")
    exam = relationship("ExamSchedule")


# ════════════════════════════════════════════════════════════════
#  AGENT 8 — Hackathon Recommendation
# ════════════════════════════════════════════════════════════════

class Hackathon(Base):
    __tablename__ = "hackathons"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    organizer = Column(String, nullable=False)
    platform = Column(String, nullable=False)  # Devfolio/Unstop/HackerEarth/MLH/Other
    mode = Column(String, default="Online")  # Online/Offline/Hybrid
    theme = Column(String, nullable=True)  # AI/Web/Mobile/Blockchain/Open
    description = Column(Text, nullable=True)
    prize_pool = Column(String, nullable=True)  # e.g. ₹1,00,000
    team_size_min = Column(Integer, default=1)
    team_size_max = Column(Integer, default=4)
    registration_deadline = Column(Date, nullable=True)
    event_start_date = Column(Date, nullable=True)
    event_end_date = Column(Date, nullable=True)
    registration_link = Column(String, nullable=True)
    eligible_departments = Column(String, nullable=True)  # All or CSE,ECE
    skill_tags = Column(String, nullable=True)  # Python,ML,React

    registrations = relationship("HackathonRegistration", back_populates="hackathon")


class HackathonRegistration(Base):
    __tablename__ = "hackathon_registrations"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    hackathon_id = Column(Integer, ForeignKey("hackathons.id"), nullable=False)
    registered_at = Column(DateTime, server_default=func.now())
    team_name = Column(String, nullable=True)
    result = Column(String, nullable=True)  # Winner/Runner-up/Participant/null

    student = relationship("Student", back_populates="hackathon_registrations")
    hackathon = relationship("Hackathon", back_populates="registrations")


# ════════════════════════════════════════════════════════════════
#  AGENT 9 — Transport Information
# ════════════════════════════════════════════════════════════════

class Bus(Base):
    __tablename__ = "buses"
    id = Column(Integer, primary_key=True, index=True)
    bus_number = Column(String, unique=True, nullable=False)
    city = Column(String, nullable=True) # Coimbatore, Tiruppur, Udumalai, Pollachi
    route_name = Column(String, nullable=False)
    capacity = Column(Integer, default=50)
    driver_name = Column(String, nullable=True)
    driver_phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    stops = relationship("BusStop", back_populates="bus", order_by="BusStop.stop_order")
    schedules = relationship("BusSchedule", back_populates="bus")
    delays = relationship("BusDelay", back_populates="bus")


class BusStop(Base):
    __tablename__ = "bus_stops"
    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)
    stop_name = Column(String, nullable=False)
    stop_order = Column(Integer, nullable=False)
    scheduled_arrival = Column(String, nullable=False)  # e.g. "08:30"
    is_spot = Column(Boolean, default=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    bus = relationship("Bus", back_populates="stops")


class BusSchedule(Base):
    __tablename__ = "bus_schedules"
    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)
    direction = Column(String, nullable=False)  # To Campus / From Campus
    departure_time = Column(String, nullable=False)
    arrival_time = Column(String, nullable=False)
    days_of_operation = Column(String, nullable=False)  # Mon-Fri / Daily

    bus = relationship("Bus", back_populates="schedules")


class BusDelay(Base):
    __tablename__ = "bus_delays"
    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)
    delay_date = Column(Date, nullable=False)
    delay_minutes = Column(Integer, nullable=False)
    reason = Column(String, nullable=True)  # Traffic/Breakdown/Weather

    bus = relationship("Bus", back_populates="delays")


class BusTicketBooking(Base):
    __tablename__ = "bus_ticket_bookings"
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String, unique=True, index=True, nullable=False)
    student_id = Column(String, nullable=False)
    student_name = Column(String, nullable=False)
    hostel_block_room = Column(String, nullable=True)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)
    seat_number = Column(String, nullable=False)
    travel_date = Column(String, nullable=False)
    destination_city = Column(String, nullable=False)
    boarding_point = Column(String, nullable=False)
    drop_point = Column(String, nullable=False)
    departure_time = Column(String, nullable=False)
    contact_phone = Column(String, nullable=True)
    status = Column(String, default="CONFIRMED") # CONFIRMED / CANCELLED
    qr_code_data = Column(String, nullable=True)


# ════════════════════════════════════════════════════════════════
#  AGENT 10 — Feedback Collection
# ════════════════════════════════════════════════════════════════

class FeedbackForm(Base):
    __tablename__ = "feedback_forms"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    target_type = Column(String, nullable=False)  # Faculty/Course/Hostel/Cafeteria/General
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    responses = relationship("FeedbackResponse", back_populates="form")


class FeedbackResponse(Base):
    __tablename__ = "feedback_responses"
    id = Column(Integer, primary_key=True, index=True)
    form_id = Column(Integer, ForeignKey("feedback_forms.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    rating = Column(Float, nullable=False)  # 1-5
    feedback_text = Column(Text, nullable=True)
    sentiment = Column(String, nullable=True)  # Positive/Negative/Neutral
    sentiment_score = Column(Float, nullable=True)  # -1.0 to 1.0
    submitted_at = Column(DateTime, server_default=func.now())

    form = relationship("FeedbackForm", back_populates="responses")
    student = relationship("Student", back_populates="feedback_responses")
    faculty = relationship("Faculty", back_populates="feedback_responses")
    course = relationship("Course", back_populates="feedback_responses")


# ════════════════════════════════════════════════════════════════
#  AGENT 11 — Alumni Connect
# ════════════════════════════════════════════════════════════════

class Alumni(Base):
    __tablename__ = "alumni"
    id = Column(Integer, primary_key=True, index=True)
    alumni_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    graduation_year = Column(Integer, nullable=False)
    current_company = Column(String, nullable=True)
    current_role = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    experience_years = Column(Integer, default=0)
    location = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    email = Column(String, nullable=True)
    is_mentor = Column(Boolean, default=True)
    bio = Column(Text, nullable=True)
    expertise_areas = Column(String, nullable=True)  # ML,Backend,Startup,Finance

    skills = relationship("AlumniSkill", back_populates="alumni")
    mentorship_requests = relationship("MentorshipRequest", back_populates="alumni")


class AlumniSkill(Base):
    __tablename__ = "alumni_skills"
    id = Column(Integer, primary_key=True, index=True)
    alumni_id = Column(Integer, ForeignKey("alumni.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)

    alumni = relationship("Alumni", back_populates="skills")
    skill = relationship("Skill", back_populates="alumni_skills")


class MentorshipRequest(Base):
    __tablename__ = "mentorship_requests"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    alumni_id = Column(Integer, ForeignKey("alumni.id"), nullable=False)
    message = Column(Text, nullable=True)
    status = Column(String, default="Pending")  # Pending/Accepted/Rejected
    goal = Column(String, nullable=True)  # Placement/Research/Startup/General
    requested_at = Column(DateTime, server_default=func.now())

    student = relationship("Student", back_populates="mentorship_requests")
    alumni = relationship("Alumni", back_populates="mentorship_requests")


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

# ── Office Agent Models ───────────────────────────────────────
class FeeStatement(Base):
    __tablename__ = "fee_statements"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    semester = Column(Integer, nullable=False)
    current_semester_fee = Column(Float, nullable=False)
    total_fee = Column(Float, nullable=False)
    paid_amount = Column(Float, nullable=False)
    pending_balance = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    late_fee = Column(Float, default=0.0)
    fee_breakdown = Column(JSON, nullable=True) # e.g. {"Tuition": 45000, "Transport": 12000, ...}
    payment_history = Column(JSON, nullable=True) # e.g. list of past transactions

class CertificateRequest(Base):
    __tablename__ = "certificate_requests"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    certificate_type = Column(String, nullable=False) # e.g. "Bonafide", "Study", etc.
    status = Column(String, default="Submitted") # "Submitted", "Under Verification", "Approved", "Rejected", "Ready for Collection"
    application_number = Column(String, unique=True, index=True, nullable=False)
    created_date = Column(DateTime, server_default=func.now())
    estimated_completion_date = Column(Date, nullable=True)
    remarks = Column(Text, nullable=True)

class OfficeRequest(Base):
    __tablename__ = "office_requests"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    request_type = Column(String, nullable=False) # e.g. "ID Card Reissue", "Bus Pass Request"
    request_number = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, default="Pending")
    remarks = Column(Text, nullable=True)
    created_date = Column(DateTime, server_default=func.now())
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

class OfficeDocument(Base):
    __tablename__ = "office_documents"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    document_name = Column(String, nullable=False)
    document_type = Column(String, nullable=False) # "Receipt", "Statement", "Circular"
    download_url = Column(String, nullable=False)
    created_date = Column(DateTime, server_default=func.now())

class OfficeAnnouncement(Base):
    __tablename__ = "office_announcements"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    announcement_type = Column(String, nullable=False) # "Holiday", "Deadline", "Circular"
    content = Column(Text, nullable=False)
    publish_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=True)
