from sqlalchemy.orm import Session
from app.models.models import (
    Building, CampusRoute, Book, Department,
    FoodItem, CafeteriaMenu, MessMenu
)
import random

def seed_campus(db: Session):
    print("Seeding Campus Navigation Graph...")
    buildings_list = db.query(Building).all()
    b_map = {b.name: b for b in buildings_list}
    
    connections = [
        ("Main Gate", "Main Block"),
        ("Main Gate", "AI Block"),
        ("Main Block", "Office Room"),
        ("Main Block", "Playground"),
        ("AI Block", "Mech Block"),
        ("AI Block", "Boys Hostel A Block"),
        ("Mech Block", "Office Room"),
        ("Office Room", "Amenity Center"),
        ("Office Room", "Xerox Shop"),
        ("Amenity Center", "Playground"),
        ("Amenity Center", "Xerox Shop"),
        ("Xerox Shop", "Cafe Corner"),
        ("Cafe Corner", "Medical Center"),
        ("Cafe Corner", "Tea Shop"),
        ("Medical Center", "Girls Hostel A Block"),
        ("Tea Shop", "Mario"),
        ("Mario", "Girls Hostel C Block"),
        ("Playground", "Drone Block"),
        ("Boys Hostel A Block", "Boys Hostel B Block"),
        ("Boys Hostel A Block", "Boys Hostel C Block"),
        ("Boys Hostel C Block", "Boys Hostel D Block"),
        ("Girls Hostel A Block", "Girls Hostel B Block"),
        ("Girls Hostel A Block", "Girls Hostel C Block")
    ]

    for name1, name2 in connections:
        b1 = b_map.get(name1)
        b2 = b_map.get(name2)
        if b1 and b2:
            # Simple euclidean distance calculation for lat/lng
            dist = ((b1.latitude - b2.latitude)**2 + (b1.longitude - b2.longitude)**2)**0.5 * 1000
            walk_time = max(1.0, round(dist / 80.0, 1))
            
            # Bidirectional routes
            for s, d in [(b1, b2), (b2, b1)]:
                exists = db.query(CampusRoute).filter_by(source_id=s.id, destination_id=d.id).first()
                if not exists:
                    db.add(CampusRoute(
                        source_id=s.id,
                        destination_id=d.id,
                        distance_meters=round(dist, 1),
                        walk_time_minutes=walk_time,
                        path_description=f"Walkway between {s.name} and {d.name}"
                    ))
    db.commit()

    print("Seeding Library (15000 books)...")
    departments = db.query(Department).all()
    if departments:
        # Fast bulk insert
        books = []
        prefixes = ["Introduction to", "Advanced", "Principles of", "Applied", "Modern", "Fundamentals of"]
        for i in range(1, 15001):
            dept = random.choice(departments)
            word = dept.department_name.split()[0]
            title = f"{random.choice(prefixes)} {word} Vol {random.randint(1,5)}"
            books.append(Book(
                isbn=f"978-{random.randint(1000000000, 9999999999)}",
                title=title,
                author=f"Author {random.randint(1, 1000)}",
                department_id=dept.id,
                rack_number=f"Rack-{dept.department_id}-{random.randint(1, 50)}",
                total_copies=random.randint(1, 10),
                available_copies=random.randint(1, 10)
            ))
            if i % 5000 == 0:
                db.bulk_save_objects(books)
                books = []
        if books:
            db.bulk_save_objects(books)
        db.commit()

    print("Seeding Food Items & Cafeteria Menu...")
    food_data = [
        {"name": "Masala Dosa", "cat": "Main", "cuisine": "South Indian", "price": 50, "cal": 350, "pro": 8, "veg": True},
        {"name": "Idli", "cat": "Snack", "cuisine": "South Indian", "price": 30, "cal": 150, "pro": 4, "veg": True},
        {"name": "Pongal", "cat": "Main", "cuisine": "South Indian", "price": 40, "cal": 400, "pro": 9, "veg": True},
        {"name": "Poori", "cat": "Main", "cuisine": "South Indian", "price": 45, "cal": 450, "pro": 7, "veg": True},
        {"name": "Veg Meals", "cat": "Main", "cuisine": "Indian", "price": 70, "cal": 600, "pro": 15, "veg": True},
        {"name": "Chicken Biryani", "cat": "Main", "cuisine": "Indian", "price": 120, "cal": 800, "pro": 35, "veg": False},
        {"name": "Paneer Butter Masala", "cat": "Main", "cuisine": "Indian", "price": 90, "cal": 500, "pro": 18, "veg": True},
        {"name": "Lemon Rice", "cat": "Main", "cuisine": "South Indian", "price": 40, "cal": 300, "pro": 6, "veg": True},
        {"name": "Curd Rice", "cat": "Main", "cuisine": "South Indian", "price": 40, "cal": 250, "pro": 5, "veg": True},
        {"name": "Parotta", "cat": "Main", "cuisine": "South Indian", "price": 15, "cal": 200, "pro": 4, "veg": True},
        {"name": "Coffee", "cat": "Beverage", "cuisine": "Indian", "price": 15, "cal": 100, "pro": 2, "veg": True},
        {"name": "Tea", "cat": "Beverage", "cuisine": "Indian", "price": 12, "cal": 80, "pro": 1, "veg": True},
        {"name": "Fresh Juice", "cat": "Beverage", "cuisine": "Continental", "price": 40, "cal": 150, "pro": 1, "veg": True},
        {"name": "Milkshake", "cat": "Beverage", "cuisine": "Continental", "price": 60, "cal": 300, "pro": 8, "veg": True},
        {"name": "Pizza", "cat": "Snack", "cuisine": "Continental", "price": 150, "cal": 800, "pro": 20, "veg": True},
        {"name": "Burger", "cat": "Snack", "cuisine": "Fast Food", "price": 80, "cal": 500, "pro": 15, "veg": False},
        {"name": "Sandwich", "cat": "Snack", "cuisine": "Fast Food", "price": 50, "cal": 350, "pro": 10, "veg": True}
    ]
    
    db_foods = []
    for f in food_data:
        food = FoodItem(
            name=f["name"],
            category=f["cat"],
            cuisine=f["cuisine"],
            is_veg=f["veg"],
            price=f["price"],
            calories=f["cal"],
            protein_g=f["pro"],
            avg_rating=round(random.uniform(3.5, 5.0), 1)
        )
        db.add(food)
        db_foods.append(food)
    db.commit()

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    slots = ["Breakfast", "Lunch", "Snacks", "Dinner"]
    
    # Cafeteria Menu
    for day in days:
        for slot in slots:
            selected = random.sample(db_foods, k=5)
            for item in selected:
                db.add(CafeteriaMenu(
                    food_item_id=item.id,
                    day_of_week=day,
                    meal_slot=slot,
                    is_available=True
                ))
                
    # Mess Menu (weekly rotating)
    for day in days:
        for slot in slots:
            db.add(MessMenu(
                day_of_week=day,
                meal_type=slot,
                items=", ".join([random.choice(db_foods).name for _ in range(3)]),
                calories=random.randint(200, 600),
                protein_g=random.uniform(5, 20),
                is_veg=random.choice([True, False]),
                healthy_rating=random.uniform(3.0, 5.0),
                calories_approx=random.randint(200, 600)
            ))
    db.commit()
