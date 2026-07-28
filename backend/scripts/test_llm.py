from app.agents.orchestrator import _detect_intent

def test_llm_orchestrator():
    queries = [
        "I want to file a complaint about the food in my room",
        "What time is my operating systems class?",
        "How do I reach the main library from the CS block?",
        "Can you predict my attendance shortage?",
        "When is the next hackathon happening?"
    ]
    
    print("Loading LLM and testing intents...")
    for q in queries:
        print(f"\nQuery: {q}")
        intent = _detect_intent(q)
        print(f"Detected Intent: {intent}")

if __name__ == "__main__":
    test_llm_orchestrator()
