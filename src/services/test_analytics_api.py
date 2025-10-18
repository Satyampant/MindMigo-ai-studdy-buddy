"""
Test script for /progress/analytics endpoint
Run: python -m src.services.test_analytics_api
"""
import requests
import json

BASE_URL = "http://localhost:8000"
STUDENT_ID = "student_123"

# First, record some test attempts
print("Step 1: Recording test quiz attempts...")
test_attempts = [
    {"student_id": STUDENT_ID, "topic": "Python", "difficulty": "easy", 
     "questions": ["Q1", "Q2", "Q3"], "user_answers": ["A1", "A2", "A3"], 
     "correct_answers": ["A1", "A2", "A3"]},
    {"student_id": STUDENT_ID, "topic": "Python", "difficulty": "medium", 
     "questions": ["Q1", "Q2"], "user_answers": ["A1", "Wrong"], 
     "correct_answers": ["A1", "A2"]},
    {"student_id": STUDENT_ID, "topic": "Machine Learning", "difficulty": "hard", 
     "questions": ["Q1", "Q2", "Q3", "Q4"], "user_answers": ["A1", "Wrong", "A3", "Wrong"], 
     "correct_answers": ["A1", "A2", "A3", "A4"]},
]

for attempt in test_attempts:
    response = requests.post(f"{BASE_URL}/progress/record", json=attempt)
    print(f"  ✓ Recorded: {attempt['topic']} ({attempt['difficulty']}) - Status: {response.status_code}")

# Now fetch analytics
print(f"\nStep 2: Fetching analytics for {STUDENT_ID}...")
response = requests.get(f"{BASE_URL}/progress/analytics/{STUDENT_ID}")

if response.status_code == 200:
    result = response.json()
    print(f"\n✅ Success! Analytics Response:\n")
    print(json.dumps(result, indent=2))
else:
    print(f"\n❌ Failed! Status: {response.status_code}")
    print(response.text)
