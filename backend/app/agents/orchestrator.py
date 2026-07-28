import json
import re
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

def _extract_intent_and_entities(query: str, session_context: dict) -> dict:
    """Extract intent and entities using LLM."""
    llm = get_llm()
    if not llm:
        return {"intent": "general"}

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
        # Find JSON block
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return data
    except Exception as e:
        print(f"Extraction error: {e}")
        
    return {"intent": "general", "entities": {}}


def query_orchestrator(query: str, student_id: str, session_id: str = "default") -> str:
    """Main orchestrator entry point with memory and hybrid routing."""
    db = _get_db()
    try:
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
            # Truncate to avoid context window crashes
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
            print(f"DEBUG PROMPT LENGTH: {len(prompt)}")
            try:
                response = llm(prompt, max_tokens=250, stop=["<|im_end|>"], temperature=0.1)
                answer = response['choices'][0]['text'].strip()
                return answer
            except Exception as e:
                print(f"LLM Generation error: {e}")
                return f"Error generating response: {e}"

        return f"Database Data: {json.dumps(json_data, default=str)}"

    except Exception as e:
        return f"🤖 Orchestrator encountered an error: {str(e)}"
    finally:
        db.close()
