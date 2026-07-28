import re

file_path = "scripts/seed_db.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Hackathon block
old_hack = """"organizer": "Tech Club", "venue": "CS Lab", "registration_link": "http://hack.com"})"""
new_hack = """"organizer": "Tech Club", "venue": "CS Lab", "registration_link": "http://hack.com", "platform": "Devfolio"})"""
content = content.replace(old_hack, new_hack)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Patched seed_db.py Hackathon successfully!")
