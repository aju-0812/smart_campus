import re

file_path = "scripts/seed_db.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace MessMenu block
old_mess = """"meal_type": slot, "item_name": f"Mess Meal {i} {slot}", "calories": 400, "protein_g": 15.0, "is_veg": True, "healthy_rating": 4.0})"""
new_mess = """"meal_type": slot, "items": f"Mess Meal {i} {slot}", "calories": 400, "protein_g": 15.0, "is_veg": True, "healthy_rating": 4.0})"""
content = content.replace(old_mess, new_mess)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Patched seed_db.py successfully again!")
