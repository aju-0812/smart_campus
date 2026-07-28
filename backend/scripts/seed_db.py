import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base, SessionLocal
from scripts.seeders.seed_academics import seed_academics
from scripts.seeders.seed_students import seed_students
from scripts.seeders.seed_campus import seed_campus
from scripts.seeders.seed_events import seed_events
from scripts.seeders.seed_timetable import seed_timetable
from app.models.models import University

def main():
    print("Dropping all existing tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creating tables based on new schema...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("Seeding University Info...")
        db.add(University(
            name="Smart Campus Institute of Technology",
            campus_address="123 Tech City, Bangalore 560100",
            website="https://smartcampus.edu",
            email="admin@smartcampus.edu",
            phone="+91-80-12345678",
            vision="To be a global leader in technology education and innovation.",
            mission="Empowering students through cutting-edge research, hands-on learning, and industry collaboration.",
            principal="Dr. APJ Srinivasan",
            vice_principal="Dr. Radhakrishnan",
            dean_academics="Dr. S. Ramaswamy",
            dean_students="Dr. V. N. Rao",
            registrar="Mr. K. K. Menon",
            working_hours="Monday - Friday: 08:30 AM to 05:00 PM",
            campus_map_url="https://smartcampus.edu/map.png"
        ))
        db.commit()

        print("--- Initiating Massive Production Seeding ---")
        seed_academics(db)
        seed_students(db)
        seed_campus(db)
        seed_events(db)
        seed_timetable(db)
        
        print("SUCCESS: Database successfully seeded with realistic, zero-conflict data!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
