"""
Test script for /progress/record endpoint
Run: python -m src.services.test_progress_api
"""
import requests
import json

API_URL = "http://localhost:8000/progress/record"

test_data = {
    "student_id": "student_123",
    "topic": "Python Programming",
    "difficulty": "medium",
    "questions": ["What is a list?", "What is a dict?", "What is a tuple?"],
    "user_answers": ["mutable sequence", "key-value pairs", "immutable sequence"],
    "correct_answers": ["mutable sequence", "key-value pairs", "immutable sequence"]
}

print("Testing /progress/record endpoint...")
print(f"Request: {json.dumps(test_data, indent=2)}")

response = requests.post(API_URL, json=test_data)

if response.status_code == 200:
    result = response.json()
    print(f"\n✅ Success! Response:")
    print(json.dumps(result, indent=2, default=str))
else:
    print(f"\n❌ Failed! Status: {response.status_code}")
    print(response.text)
