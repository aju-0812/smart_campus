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
    {"name": "Main Gate", "type": "Gate", "lat": 0.8, "lng": 4.5},
    {"name": "Main Block", "type": "Academic", "lat": 2.5, "lng": 3.5},
    {"name": "AI Block", "type": "Academic", "lat": 2.2, "lng": 5.6},
    {"name": "Mech Block", "type": "Academic", "lat": 3.4, "lng": 5.6},
    {"name": "Office Room", "type": "Admin", "lat": 4.2, "lng": 4.7},
    {"name": "Amenity Center", "type": "Academic", "lat": 5.5, "lng": 4.5},
    {"name": "Xerox Shop", "type": "Academic", "lat": 5.3, "lng": 5.3},
    {"name": "Cafe Corner", "type": "Cafeteria", "lat": 5.3, "lng": 5.9},
    {"name": "Medical Center", "type": "Medical", "lat": 5.3, "lng": 6.5},
    {"name": "Tea Shop", "type": "Cafeteria", "lat": 6.4, "lng": 5.4},
    {"name": "Mario", "type": "Misc", "lat": 6.4, "lng": 6.0},
    {"name": "Playground", "type": "Sports", "lat": 5.1, "lng": 3.0},
    {"name": "Drone Block", "type": "Academic", "lat": 6.7, "lng": 2.8},
    {"name": "Boys Hostel A Block", "type": "Hostel", "lat": 2.2, "lng": 7.5},
    {"name": "Boys Hostel B Block", "type": "Hostel", "lat": 2.2, "lng": 8.3},
    {"name": "Boys Hostel C Block", "type": "Hostel", "lat": 3.3, "lng": 7.5},
    {"name": "Boys Hostel D Block", "type": "Hostel", "lat": 3.3, "lng": 8.3},
    {"name": "Girls Hostel A Block", "type": "Hostel", "lat": 5.4, "lng": 7.5},
    {"name": "Girls Hostel B Block", "type": "Hostel", "lat": 5.4, "lng": 8.2},
    {"name": "Girls Hostel C Block", "type": "Hostel", "lat": 6.3, "lng": 7.9}
]

FACULTY_FIRST_NAMES = ["Priya", "Arjun", "Meena", "Rahul", "Anjali", "Vikram", "Sneha", "Rohan", "Kavya", "Siddharth", "Neha", "Aditya", "Pooja", "Karan", "Shruti"]
FACULTY_LAST_NAMES = ["Raman", "Kumar", "Singh", "Sharma", "Verma", "Patel", "Reddy", "Nair", "Iyer", "Menon", "Joshi", "Das", "Bose", "Gupta", "Rao"]

DESIGNATIONS = ["Professor", "Associate Professor", "Assistant Professor", "Lecturer"]

REALISTIC_COURSES = {
    "AIDS": [
        "Introduction to AI", "Python for Data Science", "Data Science Lab", "Applied Statistics", "Linear Algebra for ML",
        "Machine Learning", "Data Mining & Warehousing", "Deep Learning", "Big Data Analytics", "Optimization Techniques",
        "Natural Language Processing", "Computer Vision Algorithms", "Reinforcement Learning", "Predictive Analytics", "AI Ethics & Governance",
        "Neural Networks", "Data Science Pipeline", "Time Series Analysis", "Pattern Recognition", "AI in Healthcare",
        "Recommendation Systems", "Generative AI Models", "Cognitive Computing", "Data Science Seminar", "Capstone AI Project"
    ],
    "CSE": [
        "Programming in C", "Data Structures", "Design & Analysis of Algorithms", "Discrete Mathematics", "Digital Logic Design",
        "Operating Systems", "Computer Networks", "Database Management Systems", "Object Oriented Programming", "Computer Architecture",
        "Software Engineering", "Compiler Design", "Theory of Computation", "Web Technology", "Cloud Computing",
        "Cryptography & Security", "Distributed Systems", "Mobile Application Dev", "Internet of Things", "Artificial Intelligence",
        "Network Security", "Information Retrieval", "Human Computer Interaction", "Software Testing", "Systems Programming"
    ],
    "IT": [
        "Basics of Information Tech", "Web Programming", "Java Programming", "Database Administration", "Information Coding",
        "Network Protocols", "Software Engineering Principles", "System Administration", "IT Project Management", "Cloud Infrastructure",
        "E-Commerce & Security", "Multimedia Systems", "Enterprise Computing", "Data Warehousing", "Cyber Security & Forensics",
        "Mobile Computing", "Web Services & SOA", "IT Infrastructure Design", "User Interface Design", "Distributed Databases"
    ],
    "MECH": [
        "Engineering Mechanics", "Thermodynamics", "Strength of Materials", "Fluid Mechanics", "Kinematics of Machinery",
        "Manufacturing Technology", "Heat & Mass Transfer", "Design of Machine Elements", "CAD/CAM Principles", "Dynamics of Machinery",
        "Automobile Engineering", "Mechatronics Systems", "Power Plant Engineering", "Refrigeration & AC", "Fluid Power Systems",
        "Industrial Engineering", "Finite Element Analysis", "Computational Fluid Dynamics", "Turbomachinery", "Composite Materials"
    ],
    "CIVIL": [
        "Engineering Surveying", "Building Materials", "Mechanics of Fluids", "Structural Analysis", "Concrete Technology",
        "Geotechnical Engineering", "Transportation Engineering", "Environmental Engineering", "Design of Steel Structures", "Hydrology & Water Resources",
        "Foundation Engineering", "Construction Planning & Mgmt", "Bridge Engineering", "Prestressed Concrete", "Earthquake Engineering",
        "GIS & Remote Sensing", "Town Planning", "Environmental Impact Assessment", "Railways & Airports", "Structural Dynamics"
    ],
    "EEE": [
        "Electric Circuits", "Electromagnetic Fields", "Electrical Machines", "Power Systems Analysis", "Control Systems",
        "Analog & Digital Electronics", "Power Electronics", "Transmission & Distribution", "Signals & Systems", "Electrical Measurements",
        "Renewable Energy Sources", "High Voltage Engineering", "Microprocessors & MCU", "Power System Protection", "Smart Grid Technology",
        "Special Electrical Machines", "Digital Signal Processing", "Electrical Safety", "Industrial Automation", "Energy Auditing"
    ],
    "ECE": [
        "Electronic Devices & Circuits", "Digital Electronics", "Signals and Systems", "Analog Communications", "Microprocessors & Interfaces",
        "Electromagnetic Waves", "Digital Signal Processing", "Digital Communications", "VLSI Design & Technology", "Embedded Systems",
        "Antennas & Propagation", "Microwave Engineering", "Fiber Optic Communication", "Wireless Communication Systems", "Computer Communication Networks",
        "CMOS VLSI Design", "ARM System Architecture", "Radar Systems", "Satellite Communication", "RF Circuit Design"
    ],
    "BME": [
        "Anatomy & Physiology", "Biomaterials & Biocompatibility", "Biomedical Instrumentation", "Medical Sensors & Transducers", "Biosignals & Systems",
        "Biomedical Signal Processing", "Medical Image Processing", "Biomechanics & Rehabilitation", "Clinical Engineering", "Diagnostic Devices",
        "Therapeutic Equipment", "Prosthetics & Orthotics", "Biotelemetry", "Medical Electronics", "Hospital Management Systems"
    ],
    "AGRI": [
        "Soil Science & Agronomy", "Irrigation & Drainage Eng", "Farm Power & Machinery", "Post-Harvest Engineering", "Crop Physiology & Biochemistry",
        "Agricultural Meteorology", "Soil & Water Conservation", "Food Process Engineering", "Sustainable Agriculture", "Dairy Technology",
        "Tractor & Power Systems", "Greenhouse Technology", "Agro-Chemicals", "Farm Business Management", "Precision Farming"
    ],
    "CHEM": [
        "Chemical Process Calculations", "Fluid Flow Operations", "Chemical Technology", "Mechanical Unit Operations", "Chemical Thermodynamics",
        "Heat Transfer Operations", "Mass Transfer Operations", "Chemical Reaction Engineering", "Process Dynamics & Control", "Transport Phenomena",
        "Plant Design & Economics", "Safety in Chemical Plants", "Petroleum Refining Eng", "Polymer Technology", "Wastewater Treatment"
    ],
    "FOOD": [
        "Food Microbiology", "Food Chemistry & Nutrition", "Principles of Food Preservation", "Dairy Products Technology", "Bakery & Confectionery Tech",
        "Food Packaging Technology", "Food Quality & Safety Assurance", "Fruit & Vegetable Tech", "Cereal & Pulses Tech", "Beverage Technology",
        "Meat and Poultry Processing", "Food Additives & Toxicology", "Sensory Evaluation", "Food Laws & Regulations", "Nutraceuticals"
    ],
    "MBA": [
        "Marketing Management", "Financial Accounting & Analysis", "Human Resource Management", "Organizational Behavior", "Strategic Management",
        "Operations & Supply Chain", "Business Analytics", "Managerial Economics", "Financial Management", "Consumer Behavior",
        "Corporate Governance & Ethics", "Entrepreneurship Development", "Services Marketing", "International Business", "Project Management"
    ],
    "MCA": [
        "Java Programming & OOP", "Advanced Database Management", "Web Technologies", "Linux System Administration", "Python Programming",
        "Software Engineering Practices", "Data Analytics & Mining", "Cloud Computing Architectures", "Information Security", "Software Architecture",
        "Design Patterns", "NoSQL Databases", "Mobile App Development", "Big Data Analytics", "DevOps & Agility"
    ],
    "PHY": [
        "Classical Mechanics", "Electromagnetism Theory", "Quantum Mechanics Foundations", "Thermodynamics & Statistical", "Solid State Physics",
        "Nuclear & Particle Physics", "Mathematical Physics", "Optics & Spectroscopy", "Laser Physics & Applications", "Nanotechnology"
    ],
    "MATH": [
        "Linear Algebra & Matrices", "Calculus & Real Analysis", "Ordinary Differential Equations", "Probability & Statistics", "Complex Analysis",
        "Numerical Methods", "Operations Research Models", "Abstract Algebra", "Discrete Mathematics", "Topology & Functional Analysis"
    ],
    "CHEM_SCI": [
        "Organic Chemistry Basics", "Inorganic Chemistry Theory", "Physical Chemistry Concepts", "Analytical Chemistry Methods", "Polymer Chemistry",
        "Environmental Chemistry", "Biochemistry Principles", "Industrial & Applied Chemistry", "Spectroscopic Techniques", "Nanomaterials"
    ],
    "ENG": [
        "Technical Communication Skills", "Professional English", "Literature & Society Studies", "Creative Writing", "English for Career Success",
        "Soft Skills & Personality", "Introduction to Linguistics", "Media and Journalism", "Business Communication", "Cross-Cultural Communication"
    ]
}

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
        b_prefix = b.name.split()[0]
        if "Admin" in b.name: b_prefix = "A"
        elif "Mechanical" in b.name: b_prefix = "M"
        elif "Civil" in b.name: b_prefix = "C"
        elif "ECE" in b.name: b_prefix = "ECE"
        elif "EEE" in b.name: b_prefix = "EEE"
        elif "AI" in b.name: b_prefix = "AI"

        for r in range(1, 31):  # 30 rooms per building
            is_lab = random.random() > 0.7
            if is_lab:
                room_name = f"Lab-{r}" if b_prefix == "A" else f"{b_prefix}-Lab-{r}"
            else:
                room_name = f"{b_prefix}-{(r // 10) + 1}{r % 10:02d}"

            room = Classroom(
                room_name=room_name,
                building=b.name,
                capacity=random.choice([30, 60, 100, 120]),
                has_smartboard=random.choice([True, False]),
                has_projector=True,
                is_lab=is_lab,
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
        dept_courses = REALISTIC_COURSES.get(dept.department_code, ["General Studies"])
        for sem in range(1, 9):
            for c in range(5):  # 5 courses per sem
                course_type = "Theory" if c < 3 else "Lab" if c == 3 else "Elective"
                idx = (sem - 1) * 5 + c
                course_name = dept_courses[idx % len(dept_courses)]
                
                # Suffix check to make type match name beautifully
                if course_type == "Lab" and "Lab" not in course_name:
                    course_name = f"{course_name} Lab"
                elif course_type == "Elective" and "Elective" not in course_name and "Seminar" not in course_name:
                    course_name = f"{course_name} (Elective)"

                course = Course(
                    course_id=f"{dept.department_id}{sem}0{c+1}",
                    course_name=course_name,
                    department_id=dept.id,
                    semester=sem,
                    credits=random.choice([2, 3, 4]),
                    faculty_id=random.choice(dept_faculty).id,
                    type=course_type
                )
                db.add(course)
    db.commit()
