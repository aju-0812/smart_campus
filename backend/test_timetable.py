from app.core.database import SessionLocal
from app.api.timetable import get_student_timetable

db = SessionLocal()
try:
    res = get_student_timetable("S100001", db)
    print(res)
except Exception as e:
    import traceback
    traceback.print_exc()
