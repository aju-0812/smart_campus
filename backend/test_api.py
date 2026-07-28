import requests
import json

queries = [
    "list the building blocks in our university",
    "tell about cafeteria food rating",
    "tell about hackthons available"
]

for q in queries:
    try:
        resp = requests.post("http://127.0.0.1:8000/api/v1/orchestrator/query", json={"query": q, "student_id": "S10001"})
        print(f"Q: {q}")
        print(f"A: {resp.json().get('response')}\n")
    except Exception as e:
        print(f"Error for {q}: {e}")
