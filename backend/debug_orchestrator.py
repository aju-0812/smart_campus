from app.agents.orchestrator import _extract_intent_and_entities, AGENT_FUNCTIONS, get_llm
from app.core.database import SessionLocal

queries = [
    "list the building blocks in our university",
    "tell about cafeteria food rating",
    "tell about hackthons available"
]

db = SessionLocal()
for q in queries:
    print(f"--- QUERY: {q} ---")
    extracted = _extract_intent_and_entities(q, {})
    intent = extracted.get("intent", "general")
    print(f"Extracted Intent: {intent}")
    print(f"Entities: {extracted.get('entities')}")
    
    if intent in AGENT_FUNCTIONS:
        data = AGENT_FUNCTIONS[intent](q, "S10001", db, extracted.get("entities", {}))
        print(f"Agent Data: {data}")
    else:
        print("General query. No agent data.")
    print("\n")
