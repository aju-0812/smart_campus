import json
import re
import os
import time
import torch
torch.set_num_threads(16)
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

def _office_agent_response(query: str, student_id: str, db: Session, entities: dict) -> dict:
    from app.agents.office_agent import handle_office_query
    return handle_office_query(db, student_id, query, entities)

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
    "office": _office_agent_response,
}

# Local LLM and SentenceTransformer instances
_transformer_model = None
_tinyllama_generator = None
_ref_embeddings = {}

HISTORY_FILE = "session_history.json"
CAMPUS_CACHE = {}
SESSION_HISTORY_CACHE = {}

def get_cached_data(key: str, ttl: int = 180):
    if key in CAMPUS_CACHE:
        val, expiry = CAMPUS_CACHE[key]
        if time.time() < expiry:
            return val
    return None

def set_cached_data(key: str, val, ttl: int = 180):
    CAMPUS_CACHE[key] = (val, time.time() + ttl)

def load_session_history(session_id: str) -> list:
    return SESSION_HISTORY_CACHE.get(session_id, [])

def save_session_history(session_id: str, history: list):
    SESSION_HISTORY_CACHE[session_id] = history[-6:] # Keep last 6 turns (3 complete QA pairs)

def get_transformer_model():
    global _transformer_model
    if _transformer_model is None:
        from sentence_transformers import SentenceTransformer
        _transformer_model = SentenceTransformer('all-MiniLM-L6-v2')
    return _transformer_model

def get_tinyllama_generator():
    global _tinyllama_generator
    if _tinyllama_generator is None:
        from transformers import pipeline
        _tinyllama_generator = pipeline('text-generation', model='TinyLlama/TinyLlama-1.1B-Chat-v1.0', device=-1)
    return _tinyllama_generator

REFERENCE_QUERIES = {
    "timetable": [
        "what is my timetable today",
        "show my timetable",
        "what classes do i have today",
        "when is my next lab",
        "what subject do i have after lunch",
        "who teaches period 3",
        "what is my schedule",
        "my classes tomorrow",
        "timetable for tomorrow"
    ],
    "attendance": [
        "what is my attendance",
        "how many classes can i miss",
        "predict my attendance shortage",
        "am i safe from debarment",
        "will i be debarred",
        "check my attendance percentage",
        "attendance risk analysis"
    ],
    "navigation": [
        "how do i get to the library",
        "navigation route from main block to hostel",
        "where is the amenity center",
        "find route to xerox shop",
        "shortest path to drone block",
        "campus map navigation"
    ],
    "hostel": [
        "what is my hostel room",
        "which hostel block am i allocated to",
        "what is the mess menu today",
        "who is my hostel warden",
        "file a complaint about my room"
    ],
    "cafeteria": [
        "recommend lunch today",
        "what can i eat in the cafeteria",
        "canteen food menu today",
        "canteen recommendation for lunch",
        "is there veg food today"
    ],
    "placement": [
        "will i be eligible for placements",
        "what is my placement readiness score",
        "mock interview feedback",
        "which companies am i eligible for",
        "placement resume score"
    ],
    "exam": [
        "do i have any exams next week",
        "when is my next exam",
        "download my exam hall ticket",
        "what is my current gpa",
        "exam results and gpa"
    ],
    "hackathon": [
        "recommend any coding contests",
        "are there hackathons coming up",
        "hackathon matching my skills",
        "when is the next hackathon"
    ],
    "transport": [
        "which bus should i take tomorrow morning",
        "track daily college bus route",
        "is there any bus delay prediction",
        "college daily bus timetable",
        "bus routes from coimbatore"
    ],
    "feedback": [
        "give feedback for course",
        "faculty feedback evaluation rating",
        "sentiment of campus feedback"
    ],
    "alumni": [
        "connect with alumni mentor",
        "recommend an industry mentor",
        "alumni mentorship programs"
    ],
    "office": [
        "what is the fee due this semester",
        "can i apply for a bonafide certificate",
        "apply for bonafide or study certificate",
        "request an id card reissue",
        "office announcements and circulars",
        "is tomorrow a holiday",
        "no dues certificate request status"
    ]
}

def get_llm():
    try:
        return get_tinyllama_generator()
    except:
        return None

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

def _detect_intents_semantically(query: str, session_context: dict) -> list:
    q = query.lower()
    triggered = set()
    
    # 1. Keyword check for strong indicator mappings
    keyword_mappings = {
        "timetable": ["timetable", "schedule", "class", "period", "routine", "teach", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"],
        "attendance": ["attendance", "present", "absent", "debar", "shortage", "percentage"],
        "navigation": ["route", "map", "navigation", "direction", "where is", "building", "block", "find room", "path"],
        "hostel": ["hostel", "room", "mess", "warden", "complaint", "mess menu"],
        "cafeteria": ["cafeteria", "canteen", "food", "menu", "lunch", "dinner", "breakfast", "eat"],
        "placement": ["placement", "job", "career", "interview", "readiness", "resume", "company"],
        "exam": ["exam", "test", "result", "grade", "gpa", "cgpa", "ticket", "hall ticket"],
        "hackathon": ["hackathon", "coding contest", "competition"],
        "transport": ["bus", "transport", "shuttle", "delay", "stop"],
        "feedback": ["feedback", "form", "rating", "sentiment"],
        "alumni": ["mentor", "alumni", "connect"],
        "office": ["fee", "pending", "dues", "pay", "payment", "receipt", "bonafide", "circular", "announcement", "id card", "bus pass", "holiday"]
    }
    
    for intent, kw_list in keyword_mappings.items():
        if any(k in q for k in kw_list):
            triggered.add(intent)
            
    # 2. Semantic Similarity check
    try:
        model = get_transformer_model()
        global _ref_embeddings
        if not _ref_embeddings:
            for intent, refs in REFERENCE_QUERIES.items():
                _ref_embeddings[intent] = model.encode(refs, convert_to_tensor=True)
                
        query_emb = model.encode(query, convert_to_tensor=True)
        
        from sentence_transformers.util import cos_sim
        intent_scores = {}
        for intent, ref_embs in _ref_embeddings.items():
            sims = cos_sim(query_emb, ref_embs)
            intent_scores[intent] = float(sims.max())
            
        # Rank intents by similarity score
        sorted_intents = sorted(intent_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Add up to 2 semantic intents with a balanced threshold of 0.45
        added_count = 0
        for intent, score in sorted_intents:
            if score >= 0.45:
                if intent not in triggered:
                    triggered.add(intent)
                    added_count += 1
                if added_count >= 2:
                    break
    except Exception as e:
        print(f"Semantic similarity error: {e}")
        
    # 3. Contextual reinforcement
    last_agent = session_context.get("last_agent")
    if last_agent == "timetable" and any(k in q for k in ["period", "teach", "class", "who"]):
        triggered.add("timetable")
    if last_agent == "office" and any(k in q for k in ["request", "status", "apply"]):
        triggered.add("office")
        
    return list(triggered)

def _fallback_response_formatter(intent: str, json_data: dict, query: str) -> str:
    if "error" in json_data:
        return f"I couldn't complete that request because of a database connection issue. Please try again."
        
    q = query.lower()
    if intent == "timetable":
        classes = json_data.get("classes", [])
        if not classes:
            return "I couldn't find any classes scheduled in your timetable for today."
        period_match = re.search(r'period\s*(\d+)', q)
        if period_match:
            p_num = int(period_match.group(1))
            if p_num <= len(classes):
                c = classes[p_num - 1]
                return f"For Period {p_num}, you have {c.get('course')} in Room {c.get('room')} taught by {c.get('faculty')} ({c.get('time')})."
            return f"You have only {len(classes)} periods scheduled."
        res = "Here is your class timetable:\n"
        for i, c in enumerate(classes):
            res += f"  - Period {i+1}: {c.get('course')} in Room {c.get('room')} ({c.get('time')} - HOD: {c.get('faculty')})\n"
        return res
        
    elif intent == "attendance":
        pct = json_data.get("attendance_percentage", 75.0)
        total = json_data.get("total_classes", 0)
        attended = json_data.get("classes_attended", 0)
        status = json_data.get("status", "Satisfactory")
        alert = json_data.get("message", "")
        return f"Your overall attendance is currently {pct}% ({attended} out of {total} classes attended). The status is marked as {status}. {alert}"
        
    elif intent == "office":
        if "fee_info" in json_data:
            f = json_data["fee_info"]
            return f"Your total fee statement is Rs. {f.get('total_fee')}. You have paid Rs. {f.get('paid_amount')} and have a pending balance of Rs. {f.get('pending_balance')} due by {f.get('due_date')}."
        if "certificate_requests" in json_data:
            reqs = json_data["certificate_requests"]
            if reqs:
                return "Your requested certificates:\n" + "\n".join(f"  - {r['certificate_type']}: {r['status']}" for r in reqs)
            return "You have no active certificate requests."
        if "announcements" in json_data:
            ann = json_data["announcements"]
            if ann:
                return "Latest announcements:\n" + "\n".join(f"  - {a['title']} ({a['announcement_type']})" for a in ann)
            return "No announcements found."
        return "I can fetch your pending fee details, certificate applications, or announcements. Which would you like?"
        
    elif intent == "exam":
        upcoming = json_data.get("upcoming_exams", [])
        if upcoming:
            res = "Here are your upcoming examinations:\n"
            for e in upcoming[:3]:
                res += f"  - {e.get('course_name')} ({e.get('course_code')}) on {e.get('date')} at {e.get('start_time')} | Venue: {e.get('venue')}\n"
            return res
        return "There are no upcoming exams listed in your current semester schedule."
        
    elif intent == "transport":
        buses = json_data.get("available_buses", [])
        if buses:
            return f"There are {len(buses)} college daily buses active across the major routes. For Udumalpet, Udumalai, Coimbatore, and Pollachi, routes run as scheduled."
        return "No active transport buses are listed at this moment."
        
    elif intent == "hostel":
        info = json_data.get("hostel_info", {})
        menu = json_data.get("mess_menu_today", [])
        res = ""
        if info.get("hostel_allocated"):
            res += f"You are allocated to Room {info.get('room_number')} in {info.get('hostel_name')} Warden: {info.get('warden_name')}.\n"
        if menu:
            res += "Today's Mess Menu:\n" + "\n".join(f"  - {m.get('meal_type')}: {m.get('items')}" for m in menu)
        return res if res else "Hostel details could not be found."
        
    elif intent == "cafeteria":
        menu = json_data.get("menu", [])
        recs = json_data.get("recommendations", [])
        res = "Cafeteria Menu Highlights:\n"
        for m in menu[:3]:
            res += f"  - {m.get('name')} (Rs. {m.get('price')})\n"
        if recs:
            res += "Recommendations based on your profile:\n" + "\n".join(f"  - {r.get('name')}" for r in recs[:2])
        return res
        
    return f"Here is the detailed information: {json.dumps(json_data, indent=1)}"

def query_orchestrator(query: str, student_id: str, session_id: str = "default") -> str:
    """Conversational campus AI orchestrator."""
    db = _get_db()
    try:
        # Cache student profile lookups
        student_key = f"student_profile_{student_id}"
        cached_student = get_cached_data(student_key)
        if cached_student:
            class StudentMock:
                def __init__(self, **kwargs):
                    self.__dict__.update(kwargs)
            student = StudentMock(**cached_student)
        else:
            from app.models.models import Student
            student = db.query(Student).filter(Student.student_id == student_id).first()
            if student:
                student_data = {
                    "name": student.name,
                    "student_id": student.student_id,
                    "department": student.department,
                    "semester": student.semester,
                    "cgpa": student.cgpa
                }
                set_cached_data(student_key, student_data, ttl=600) # Cache student profile for 10 minutes

        # Handle Personal Queries
        personal_reply = _handle_personal_queries(query, student)
        if personal_reply:
            return personal_reply

        # Handle General Greetings & Capabilities
        general_reply = _handle_general_conversations(query)
        if general_reply:
            return general_reply

        # 1. Load Session History
        history = load_session_history(session_id)
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

        # 2. Extract Intents Semantically
        triggered_intents = _detect_intents_semantically(query, context)
        
        # 3. Handle General Knowledge Queries (if no campus agent triggered)
        if not triggered_intents:
            session.last_agent = "general"
            db.commit()
            
            generator = get_tinyllama_generator()
            
            # Format conversational prompt
            prompt = "<|system|>\nYou are a friendly, conversational academic AI assistant for Sri Eshwar College. Keep your answers concise, clear, and natural. Do not mention system internals.</s>\n"
            for turn in history[-4:]:
                role_label = "user" if turn["role"] == "user" else "assistant"
                prompt += f"<|{role_label}|>\n{turn['content']}</s>\n"
            prompt += f"<|user|>\n{query}</s>\n<|assistant|>\n"
            
            with torch.inference_mode():
                res = generator(prompt, max_new_tokens=75, stop_sequence="<|user|>", temperature=0.3)
            answer = res[0]['generated_text'].split("<|assistant|>\n")[-1].strip().split("<|")[0].strip()
            
            # Save history
            history.append({"role": "user", "content": query})
            history.append({"role": "assistant", "content": answer})
            save_session_history(session_id, history)
            return answer

        # 4. Call Triggered Campus Agents concurrently
        combined_json = {}
        agents_to_run = [intent for intent in triggered_intents if intent in AGENT_FUNCTIONS]
        
        if agents_to_run:
            from concurrent.futures import ThreadPoolExecutor
            
            entities = {}
            q_lower = query.lower()
            if "tomorrow" in q_lower:
                entities["time_filter"] = "tomorrow"
            period_match = re.search(r'period\s*(\d+)', q_lower)
            if period_match:
                entities["period_number"] = int(period_match.group(1))

            def run_single_agent(agent_name):
                # Check cache for static/safe agents
                if agent_name in ["timetable", "transport", "department", "course_catalog"] and not entities.get("period_number"):
                    cache_key = f"agent_res_{agent_name}_{student_id}"
                    cached_val = get_cached_data(cache_key)
                    if cached_val:
                        return cached_val
                
                thread_db = _get_db()
                try:
                    res = AGENT_FUNCTIONS[agent_name](query, student_id, thread_db, entities)
                    if agent_name in ["timetable", "transport", "department", "course_catalog"] and not entities.get("period_number"):
                        cache_key = f"agent_res_{agent_name}_{student_id}"
                        set_cached_data(cache_key, res, ttl=180) # Cache for 3 minutes
                    return res
                finally:
                    thread_db.close()

            with ThreadPoolExecutor(max_workers=len(agents_to_run)) as executor:
                futures = {name: executor.submit(run_single_agent, name) for name in agents_to_run}
                for name, future in futures.items():
                    combined_json[name] = future.result()
                
        # Update memory
        session.last_agent = triggered_intents[0]
        db.commit()

        # 5. Generate Merged Response
        generator = get_tinyllama_generator()
        json_str = json.dumps(combined_json, separators=(',', ':'), default=str)
        if len(json_str) > 2000:
            json_str = json_str[:2000] + "... (truncated data)"
            
        prompt = f"<|system|>\nYou are a friendly conversational assistant. Use the campus database JSON below to answer the student's question in a single cohesive, natural paragraph. Do not expose raw JSON or internal variable names. If the database is empty or says not found, explain naturally. Conciseness is key.\n\nDatabase JSON:\n{json_str}</s>\n"
        for turn in history[-3:]:
            role_label = "user" if turn["role"] == "user" else "assistant"
            prompt += f"<|{role_label}|>\n{turn['content']}</s>\n"
        prompt += f"<|user|>\n{query}</s>\n<|assistant|>\n"
        
        try:
            with torch.inference_mode():
                res = generator(prompt, max_new_tokens=85, stop_sequence="<|user|>", temperature=0.1)
            answer = res[0]['generated_text'].split("<|assistant|>\n")[-1].strip().split("<|")[0].strip()
        except Exception as e:
            print(f"TinyLlama formatting error: {e}")
            answer = _fallback_response_formatter(triggered_intents[0], combined_json.get(triggered_intents[0], {}), query)

        # Save history
        history.append({"role": "user", "content": query})
        history.append({"role": "assistant", "content": answer})
        save_session_history(session_id, history)
        return answer

    except Exception as e:
        return f"I encountered an orchestrator error while retrieval: {str(e)}"
    finally:
        db.close()
