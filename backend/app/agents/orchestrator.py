import json
import re
from typing import Optional
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.models import ConversationSession

# ── Agent response functions ──────────────────────────────────────────────────
def _get_db() -> Session:
    return SessionLocal()

def _timetable_agent_response(query: str, student_id: str, db: Session, entities: dict) -> dict:
    from app.agents.timetable_agent import handle_timetable_query
    return handle_timetable_query(db, student_id, entities)

def _attendance_agent_response(query: str, student_id: str, db: Session, entities: dict) -> dict:
    from app.agents.attendance_agent import handle_attendance_query
    return handle_attendance_query(db, student_id, entities)

def _navigation_agent_response(query: str, student_id: str, db: Session, entities: dict) -> dict:
    from app.models.models import Building
    buildings = db.query(Building).limit(5).all()
    return {"status": "ok", "known_buildings": [b.name for b in buildings]}

def _hostel_agent_response(query: str, student_id: str, db: Session, entities: dict) -> dict:
    from app.agents.hostel_agent import get_student_hostel_info, get_mess_menu
    from datetime import date
    info = get_student_hostel_info(db, student_id)
    day = date.today().strftime("%A")
    menu = get_mess_menu(db, day)
    return {"hostel_info": info, "mess_menu_today": menu}

def _cafeteria_agent_response(query: str, student_id: str, db: Session, entities: dict) -> dict:
    from app.agents.cafeteria_agent import get_menu_today, content_based_recommendations
    menu = get_menu_today(db)
    recs = content_based_recommendations(db, student_id, 3)
    return {"menu": menu, "recommendations": recs}

def _placement_agent_response(query: str, student_id: str, db: Session, entities: dict) -> dict:
    from app.agents.placement_agent import get_placement_profile, get_company_recommendations
    profile = get_placement_profile(db, student_id)
    companies = get_company_recommendations(db, student_id, 3)
    return {"profile": profile, "company_matches": companies}

def _exam_agent_response(query: str, student_id: str, db: Session, entities: dict) -> dict:
    from app.agents.exam_agent import get_exam_schedule
    return get_exam_schedule(db, student_id)

def _hackathon_agent_response(query: str, student_id: str, db: Session, entities: dict) -> dict:
    from app.agents.hackathon_agent import get_recommendations
    recs = get_recommendations(db, student_id, 3)
    return {"recommended_hackathons": recs}

def _transport_agent_response(query: str, student_id: str, db: Session, entities: dict) -> dict:
    from app.agents.transport_agent import get_all_buses
    buses = get_all_buses(db)
    return {"available_buses": buses}

def _feedback_agent_response(query: str, student_id: str, db: Session, entities: dict) -> dict:
    from app.agents.feedback_agent import get_platform_summary
    return get_platform_summary(db)

def _alumni_agent_response(query: str, student_id: str, db: Session, entities: dict) -> dict:
    from app.agents.alumni_agent import get_mentor_recommendations
    recs = get_mentor_recommendations(db, student_id, 3)
    return {"mentor_matches": recs}

def _department_agent_response(query: str, student_id: str, db: Session, entities: dict) -> dict:
    from app.agents.department_agent import handle_department_query
    return handle_department_query(db, entities)

def _faculty_agent_response(query: str, student_id: str, db: Session, entities: dict) -> dict:
    from app.agents.faculty_agent import handle_faculty_query
    return handle_faculty_query(db, entities)

def _course_catalog_agent_response(query: str, student_id: str, db: Session, entities: dict) -> dict:
    from app.agents.course_catalog_agent import handle_course_catalog_query
    return handle_course_catalog_query(db, entities)


# ── Route resolution ──────────────────────────────────────────────────────────
AGENT_FUNCTIONS = {
    "timetable": _timetable_agent_response,
    "attendance": _attendance_agent_response,
    "navigation": _navigation_agent_response,
    "hostel": _hostel_agent_response,
    "cafeteria": _cafeteria_agent_response,
    "placement": _placement_agent_response,
    "exam": _exam_agent_response,
    "hackathon": _hackathon_agent_response,
    "transport": _transport_agent_response,
    "feedback": _feedback_agent_response,
    "alumni": _alumni_agent_response,
    "department": _department_agent_response,
    "faculty": _faculty_agent_response,
    "course_catalog": _course_catalog_agent_response,
}

llm_instance = None

def get_llm():
    global llm_instance
    if llm_instance is None:
        try:
            from llama_cpp import Llama
            llm_instance = Llama(
                model_path="models/Qwen2.5-7B-Instruct-Q4_K_M.gguf",
                n_ctx=2048,
                n_gpu_layers=-1,
                verbose=False
            )
        except Exception as e:
            print(f"Failed to load LLM: {e}")
            return None
    return llm_instance


def _handle_personal_queries(query: str, student) -> Optional[str]:
    if not student:
        return None
    q = query.lower()
    
    if any(k in q for k in ["my name", "what is my name", "who am i"]):
        return f"Your name is {student.name}."
    if any(k in q for k in ["my roll number", "my roll no", "my student id", "what is my roll"]):
        return f"Your student ID is {student.student_id}."
    if any(k in q for k in ["my department", "what department am i in", "my branch", "my major"]):
        return f"You are in the {student.department} department."
    if any(k in q for k in ["what semester am i in", "my semester", "which semester"]):
        return f"You are in semester {student.semester}."
    if any(k in q for k in ["my cgpa", "what is my cgpa", "my gpa"]):
        return f"Your current CGPA is {student.cgpa}."
    if any(k in q for k in ["my profile", "my details", "tell me about myself"]):
        return f"Student Profile:\n" \
               f"Name: {student.name}\n" \
               f"ID: {student.student_id}\n" \
               f"Department: {student.department}\n" \
               f"Semester: {student.semester}\n" \
               f"CGPA: {student.cgpa}"
    return None


def _handle_general_conversations(query: str) -> Optional[str]:
    q = query.strip().lower()
    
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "greetings"]
    thanks = ["thanks", "thank you", "cheers", "appreciate it"]
    identity = ["who are you", "what is your name", "your name", "who made you"]
    capabilities = ["what can you do", "help", "what services", "features"]
    
    clean_q = re.sub(r'[^\w\s]', '', q).strip()
    if clean_q in greetings:
        return "Hello. How can I assist you with your campus services today?"
        
    if any(t in clean_q for t in thanks):
        return "You are welcome. Let me know if you need help with other campus services."
        
    if any(i in clean_q for i in identity):
        return "I am the Smart Campus AI Assistant. I help students access timetable schedules, attendance logs, exam discovery tools, hostel details, cafeteria recommendations, placements, transport updates, and alumni mentorship programs."
        
    if any(c in clean_q for c in capabilities):
        return "I can help you with the following campus services:\n" \
               "- Timetable: View class schedules, period slots, classrooms, and faculty names.\n" \
               "- Attendance: Check your attendance percentage, classes attended, and debarment risk analysis.\n" \
               "- Navigation: Find building routes, distance details, and campus layouts.\n" \
               "- Hostel: Check room allocation details, mess menu today, and file complaints.\n" \
               "- Cafeteria: View daily food menu items and food recommendation options.\n" \
               "- Placements: Analyze readiness score, mock interview data, and eligible company list.\n" \
               "- Exams: View upcoming exam schedules, countdown alerts, hall tickets, and GPA/results.\n" \
               "- Hackathons: Recommend contests matching your skill tags and check registration details.\n" \
               "- Transport: Track bus schedules, arrival times, route details, and delay predictions.\n" \
               "- Feedback: File course/faculty feedback evaluations and view platforms reviews.\n" \
               "- Alumni: Connect with industry alumni mentors by skill set criteria."
               
    return None


def _fallback_intent_classifier(query: str, session_context: dict) -> dict:
    q = query.lower()
    intent = "general"
    entities = {}
    
    last_agent = session_context.get("last_agent")
    
    is_time_filter = False
    time_filter_val = None
    if "tomorrow" in q:
        is_time_filter = True
        time_filter_val = "tomorrow"
    elif "afternoon" in q:
        is_time_filter = True
        time_filter_val = "afternoon"
    elif "first" in q:
        is_time_filter = True
        time_filter_val = "first"
        
    if last_agent == "timetable":
        if is_time_filter or any(k in q for k in ["period", "teach", "class", "room", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]):
            intent = "timetable"
            if time_filter_val:
                entities["time_filter"] = time_filter_val
            period_match = re.search(r'period\s*(\d+)', q)
            if period_match:
                entities["period_number"] = int(period_match.group(1))
            return {"intent": intent, "entities": entities}

    if any(k in q for k in ["timetable", "schedule", "class", "period", "routine", "lecture", "teach", "professor", "teacher", "room", "slot", "classroom", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]):
        intent = "timetable"
        if time_filter_val:
            entities["time_filter"] = time_filter_val
        period_match = re.search(r'period\s*(\d+)', q)
        if period_match:
            entities["period_number"] = int(period_match.group(1))
            
    elif any(k in q for k in ["attendance", "present", "absent", "risk", "debar", "shortage", "safe", "percentage", "classes attended"]):
        intent = "attendance"
        
    elif any(k in q for k in ["route", "map", "navigation", "direction", "where is", "building", "block", "find room", "distance", "dijkstra", "path"]):
        intent = "navigation"
        for b in ["library", "admin", "hostel", "sports", "cafeteria", "food court", "auditorium", "medical", "placement"]:
            if b in q:
                entities["building_name"] = b
                
    elif any(k in q for k in ["hostel", "room", "mess", "warden", "complaint", "allocat", "boys block", "girls block"]):
        intent = "hostel"
        
    elif any(k in q for k in ["cafeteria", "canteen", "food", "menu", "recommend", "lunch", "dinner", "breakfast", "eat", "order"]):
        intent = "cafeteria"
        
    elif any(k in q for k in ["placement", "job", "career", "interview", "readiness", "resume", "company", "companies", "eligib"]):
        intent = "placement"
        
    elif any(k in q for k in ["exam", "test", "result", "grade", "gpa", "sgpa", "cgpa", "ticket", "hall ticket", "admit card"]):
        intent = "exam"
        
    elif any(k in q for k in ["hackathon", "coding contest", "competition", "sprint", "event"]):
        intent = "hackathon"
        
    elif any(k in q for k in ["bus", "transport", "shuttle", "route", "delay", "stop", "estimated arrival"]):
        intent = "transport"
        
    elif any(k in q for k in ["feedback", "sentiment", "form", "survey", "rating", "faculty rating"]):
        intent = "feedback"
        
    elif any(k in q for k in ["mentor", "alumni", "connect", "graduat"]):
        intent = "alumni"
        
    elif any(k in q for k in ["department", "dept"]):
        intent = "department"
        
    elif any(k in q for k in ["faculty", "professor", "teacher", "hod", "dean", "cabin"]):
        intent = "faculty"
        if "hod" in q:
            entities["query_type"] = "hod"
            
    elif any(k in q for k in ["course", "catalog", "syllabus", "subject"]):
        intent = "course_catalog"
        
    return {"intent": intent, "entities": entities}


def _fallback_response_formatter(intent: str, json_data: dict, query: str) -> str:
    if "error" in json_data:
        return f"Error: {json_data['error']}"
        
    q = query.lower()
        
    if intent == "timetable":
        classes = json_data.get("classes", [])
        if not classes:
            return f"Timetable: {json_data.get('message', 'No classes scheduled.')}"
            
        period_match = re.search(r'period\s*(\d+)', q)
        if period_match:
            p_num = int(period_match.group(1))
            if p_num <= len(classes):
                c = classes[p_num - 1]
                return f"Period {p_num} is {c.get('course')} in Room {c.get('room')} by {c.get('faculty')} ({c.get('time')})."
            else:
                return f"You only have {len(classes)} classes scheduled for this day."
                
        for c in classes:
            c_name = c.get("course", "").lower()
            course_words = [w for w in c_name.split() if len(w) > 3]
            if course_words and any(w in q for w in course_words):
                return f"The course {c.get('course')} is taught by {c.get('faculty')} in Room {c.get('room')}."
                
        response = f"Timetable for {json_data.get('student', 'you')} ({json_data.get('day', 'Today')}):\n"
        for i, c in enumerate(classes):
            response += f"  - Period {i+1}: {c.get('time')} - {c.get('course')} in Room {c.get('room')} by {c.get('faculty')}\n"
        return response.strip()
        
    elif intent == "attendance":
        pct = json_data.get("attendance_percentage", 0.0)
        status = json_data.get("status", "Unknown")
        total = json_data.get("total_classes", 0)
        attended = json_data.get("classes_attended", 0)
        msg = json_data.get("message", "")
        return f"Attendance Summary:\n" \
               f"  - Name: {json_data.get('student_name', 'Student')}\n" \
               f"  - Overall Attendance: {pct}%\n" \
               f"  - Status: {status}\n" \
               f"  - Classes Attended: {attended}/{total}\n" \
               f"  - Alert: {msg}"
               
    elif intent == "navigation":
        if "walk_time_minutes" in json_data:
            path = " -> ".join(json_data.get("path", []))
            return f"Route Found:\n" \
                   f"  - From: {json_data.get('from')}\n" \
                   f"  - To: {json_data.get('to')}\n" \
                   f"  - Estimated Walking Time: {json_data.get('walk_time_minutes')} mins ({json_data.get('distance_estimate_meters')} meters)\n" \
                   f"  - Path: {path}"
        known = json_data.get("known_buildings", [])
        return f"Known Campus Buildings:\n" + "\n".join(f"  - {b}" for b in known)

    elif intent == "hostel":
        info = json_data.get("hostel_info", {})
        menu = json_data.get("mess_menu_today", [])
        
        response = ""
        if info.get("hostel_allocated"):
            response += f"Hostel Allocation:\n" \
                        f"  - Hostel: {info.get('hostel_name')} ({info.get('hostel_gender')} Wing)\n" \
                        f"  - Room Number: {info.get('room_number')} (Floor {info.get('floor')})\n" \
                        f"  - Warden: {info.get('warden_name')} ({info.get('warden_phone')})\n\n"
        else:
            response += f"Hostel Allocation: Not allocated.\n\n"
            
        if menu:
            response += f"Mess Menu Today:\n"
            for m in menu:
                response += f"  - {m.get('meal_type')}: {m.get('items')} (~{m.get('calories_approx')} kcal)\n"
        return response.strip()

    elif intent == "cafeteria":
        menu = json_data.get("menu", [])
        recs = json_data.get("recommendations", [])
        
        response = ""
        if menu:
            response += f"Cafeteria Menu Today:\n"
            for m in menu[:5]:
                category = "Veg" if m.get("is_veg") else "Non-Veg"
                response += f"  - {m.get('name')} ({m.get('category')}) - Rs. {m.get('price')} [{category}]\n"
            if len(menu) > 5:
                response += f"    ...and {len(menu)-5} more items.\n"
                
        if recs:
            response += f"\nRecommended Food Items:\n"
            for r in recs[:3]:
                response += f"  - {r.get('name')} (Score: {r.get('recommendation_score')}%) - {r.get('method')}\n"
        return response.strip()

    elif intent == "placement":
        profile = json_data.get("profile", {})
        matches = json_data.get("company_matches", [])
        
        response = ""
        if "readiness_score" in profile:
            response += f"Placement Readiness Profile:\n" \
                        f"  - Readiness Score: {profile.get('readiness_score')}/100\n" \
                        f"  - Resume Score: {profile.get('resume_score')}/100\n" \
                        f"  - Mock Interviews Done: {profile.get('mock_interviews_done')}\n" \
                        f"  - Internships: {profile.get('internships')}, Projects: {profile.get('projects')}\n\n"
                        
        if matches:
            response += f"Eligible Company Matches:\n"
            for m in matches[:3]:
                response += f"  - {m.get('name')} ({m.get('industry')}) - Package: {m.get('package_lpa_min')}-{m.get('package_lpa_max')} LPA (Match: {m.get('match_score')}%)\n"
        return response.strip()

    elif intent == "exam":
        upcoming = json_data.get("upcoming_exams", [])
        countdown = json_data.get("countdown")
        
        response = f"Exam Dashboard for {json_data.get('name', 'you')} (Sem {json_data.get('semester', 'N/A')}):\n"
        if countdown:
            response += f"  {countdown}\n\n"
            
        if upcoming:
            response += f"Upcoming Exams:\n"
            for e in upcoming[:3]:
                response += f"  - {e.get('course_name')} ({e.get('course_code')}) - Date: {e.get('date')} at {e.get('start_time')} | Venue: {e.get('venue')}\n"
        else:
            response += f"No upcoming exams scheduled.\n"
        return response.strip()

    elif intent == "hackathon":
        recs = json_data.get("recommended_hackathons", [])
        if not recs:
            return "Hackathons: No upcoming recommended hackathons found."
        response = "Recommended Hackathons for You:\n"
        for r in recs[:3]:
            response += f"  - {r.get('title')} by {r.get('organizer')} on {r.get('platform')}\n" \
                        f"    Prize: {r.get('prize_pool')} | Deadline: {r.get('registration_deadline')} (Match: {r.get('match_score')}%)\n"
        return response.strip()

    elif intent == "transport":
        buses = json_data.get("available_buses", [])
        if not buses:
            return "Transport: No active bus services available right now."
        response = "Active Campus Buses and Routes:\n"
        for b in buses[:5]:
            response += f"  - Bus: {b.get('bus_number')} ({b.get('route_name')}) | Driver: {b.get('driver_name')} ({b.get('driver_phone')})\n"
        return response.strip()

    elif intent == "feedback":
        total = json_data.get("total_responses", 0)
        avg_rating = json_data.get("avg_platform_rating", 0.0)
        sentiments = json_data.get("sentiment_pct", {})
        top_faculty = json_data.get("top_rated_faculty", [])
        
        response = f"Feedback System Dashboard Summary:\n" \
                   f"  - Total Submissions Analyzed: {total}\n" \
                   f"  - Average Platform Rating: {avg_rating}/5.0\n" \
                   f"  - Sentiment Breakdown: Positive {sentiments.get('Positive', 0.0)}%, Neutral {sentiments.get('Neutral', 0.0)}%, Negative {sentiments.get('Negative', 0.0)}%\n\n"
        if top_faculty:
            response += f"Top Rated Faculty:\n"
            for f in top_faculty[:3]:
                response += f"  - {f.get('name')} (Avg Rating: {f.get('avg_rating')}/5.0 from {f.get('response_count')} responses)\n"
        return response.strip()

    elif intent == "alumni":
        matches = json_data.get("mentor_matches", [])
        if not matches:
            return "Alumni Mentorship: No mentor matches available right now."
        response = "Top Alumni Mentor Recommendations for You:\n"
        for m in matches[:3]:
            dept_status = "Same Dept" if m.get("same_department") else "Cross Dept"
            response += f"  - {m.get('name')} - {m.get('current_role')} at {m.get('current_company')} ({dept_status})\n" \
                        f"    Graduated: {m.get('graduation_year')} | Skills: {', '.join(m.get('skills', []))}\n"
        return response.strip()

    elif intent == "department":
        return f"Department Profile:\n" \
               f"  - Name: {json_data.get('department_name')} ({json_data.get('department_code')})\n" \
               f"  - HOD: {json_data.get('hod')}\n" \
               f"  - Office Email: {json_data.get('office_email')} | Phone: {json_data.get('office_phone')}\n" \
               f"  - Location: {json_data.get('building')} (Floor {json_data.get('floor')})\n" \
               f"  - Description: {json_data.get('description')}"

    elif intent == "faculty":
        if "faculty_name" in json_data:
            return f"Faculty Profile:\n" \
                   f"  - Name: {json_data.get('faculty_name')} ({json_data.get('designation')})\n" \
                   f"  - Department: {json_data.get('department')}\n" \
                   f"  - Office Room: {json_data.get('office_room')} in {json_data.get('office_building')}\n" \
                   f"  - Office Hours: {json_data.get('office_hours')}\n" \
                   f"  - Qualification: {json_data.get('qualification')} ({json_data.get('experience_years')} yrs experience)\n" \
                   f"  - Contact: {json_data.get('email')} | Phone: {json_data.get('phone')}"
        elif "hod_name" in json_data:
            return f"HOD Profile:\n" \
                   f"  - Department: {json_data.get('department')}\n" \
                   f"  - HOD: {json_data.get('hod_name')}\n" \
                   f"  - Office Room: {json_data.get('office_room')} in {json_data.get('office_building')}\n" \
                   f"  - Qualification: {json_data.get('qualification')}"
        elif "faculty_members" in json_data:
            members = ", ".join(json_data.get("faculty_members", []))
            return f"Faculty Members in {json_data.get('department')}:\n" \
                   f"  - HOD: {json_data.get('hod')}\n" \
                   f"  - Staff: {members}"
        return f"Faculty Info: {json.dumps(json_data)}"

    elif intent == "course_catalog":
        if "course_name" in json_data:
            return f"Course Profile:\n" \
                   f"  - Name: {json_data.get('course_name')} ({json_data.get('course_id')})\n" \
                   f"  - Department: {json_data.get('department')} | Semester: {json_data.get('semester')}\n" \
                   f"  - Credits: {json_data.get('credits')} credits | Type: {json_data.get('type')}"
        elif "courses" in json_data:
            courses = ", ".join(json_data.get("courses", []))
            return f"Courses Offered in {json_data.get('department')}:\n" \
                   f"  - List: {courses}"
        return f"Course Catalog: {json.dumps(json_data)}"

    return f"Here is the details for your request:\n{json.dumps(json_data, indent=2)}"


def _extract_intent_and_entities(query: str, session_context: dict) -> dict:
    """Extract intent and entities using LLM or rule-based fallback."""
    llm = get_llm()
    if not llm:
        return _fallback_intent_classifier(query, session_context)

    valid_intents = list(AGENT_FUNCTIONS.keys())
    
    prompt = f"""<|im_start|>system
You are a routing agent for a University system. Classify intent and extract entities.
Valid intents: {', '.join(valid_intents)}, general.
Previous Context: {json.dumps(session_context)}
Extract entities like 'faculty_name', 'department_name', 'course_name', 'query_type', 'time_filter'.
Return ONLY valid JSON like: {{"intent": "faculty", "entities": {{"faculty_name": "Rajesh", "query_type": "hod"}}}}<|im_end|>
<|im_start|>user
Query: "{query}"<|im_end|>
<|im_start|>assistant
"""
    try:
        response = llm(prompt, max_tokens=100, stop=["<|im_end|>"], temperature=0.1)
        text = response['choices'][0]['text'].strip()
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return data
    except Exception as e:
        print(f"Extraction error: {e}")
        
    return _fallback_intent_classifier(query, session_context)


def query_orchestrator(query: str, student_id: str, session_id: str = "default") -> str:
    """Main orchestrator entry point with memory and hybrid routing."""
    db = _get_db()
    try:
        # Fetch student details for personal info
        from app.models.models import Student
        student = db.query(Student).filter(Student.student_id == student_id).first()

        # Handle Personal Queries
        personal_reply = _handle_personal_queries(query, student)
        if personal_reply:
            return personal_reply

        # Handle General Conversations
        general_reply = _handle_general_conversations(query)
        if general_reply:
            return general_reply

        # 1. Memory Management
        session = db.query(ConversationSession).filter(ConversationSession.session_id == session_id).first()
        if not session:
            session = ConversationSession(session_id=session_id)
            db.add(session)
            db.commit()
            
        context = {
            "last_agent": session.last_agent,
            "last_entity": session.last_entity,
            "last_department": session.last_department,
            "last_faculty": session.last_faculty,
            "last_course": session.last_course
        }

        # 2. Extract Intent and Entities
        extracted = _extract_intent_and_entities(query, context)
        intent = extracted.get("intent", "general")
        entities = extracted.get("entities", {})

        # Merge previous context if entities missing but intent implies it
        if not entities.get("faculty_name") and session.last_faculty:
            entities["faculty_name"] = session.last_faculty
        if not entities.get("department_name") and session.last_department:
            entities["department_name"] = session.last_department

        # Update memory
        session.last_agent = intent
        if entities.get("faculty_name"): session.last_faculty = entities["faculty_name"]
        if entities.get("department_name"): session.last_department = entities["department_name"]
        if entities.get("course_name"): session.last_course = entities["course_name"]
        db.commit()

        # 3. Call Agent (returns JSON)
        if intent in AGENT_FUNCTIONS:
            json_data = AGENT_FUNCTIONS[intent](query, student_id, db, entities)
        else:
            json_data = {"message": "General assistant query. No specific agent data."}

        # 4. Final Answer Generation (Zero Hallucination)
        llm = get_llm()
        if llm:
            json_str = json.dumps(json_data, default=str)
            if len(json_str) > 3000:
                json_str = json_str[:3000] + "... [TRUNCATED]"
                
            prompt = f"""<|im_start|>system
You are a helpful university AI assistant. Use ONLY the data in the Database JSON below to answer the user's query.
If the JSON says error, not found, or is empty, say you don't have that information. Keep answers concise.
Database JSON: {json_str}<|im_end|>
<|im_start|>user
{query}<|im_end|>
<|im_start|>assistant
"""
            try:
                response = llm(prompt, max_tokens=250, stop=["<|im_end|>"], temperature=0.1)
                answer = response['choices'][0]['text'].strip()
                return answer
            except Exception as e:
                print(f"LLM Generation error: {e}")
                return f"Error generating response: {e}"

        return _fallback_response_formatter(intent, json_data, query)

    except Exception as e:
        return f"Orchestrator encountered an error: {str(e)}"
    finally:
        db.close()
