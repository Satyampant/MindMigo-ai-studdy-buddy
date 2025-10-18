"""
Comprehensive test script for Progress Dashboard
This script:
1. Creates sample quiz attempts for a student
2. Tests the analytics endpoint
3. Opens the dashboard in browser

Run: python -m src.services.test_progress_dashboard
"""
import requests
import json
import webbrowser
import time
from datetime import datetime, timedelta

API_URL = "http://localhost:8000"
STUDENT_ID = "student_123"

def create_sample_data():
    """Create diverse quiz attempts for testing"""
    print("📝 Creating sample quiz attempts...")
    
    attempts = [
        # Python - Strong performance
        {"student_id": STUDENT_ID, "topic": "Python", "difficulty": "easy", 
         "questions": ["Q1", "Q2", "Q3"], "user_answers": ["A1", "A2", "A3"], 
         "correct_answers": ["A1", "A2", "A3"]},
        {"student_id": STUDENT_ID, "topic": "Python", "difficulty": "medium", 
         "questions": ["Q1", "Q2", "Q3", "Q4"], "user_answers": ["A1", "A2", "A3", "A4"], 
         "correct_answers": ["A1", "A2", "A3", "A4"]},
        {"student_id": STUDENT_ID, "topic": "Python", "difficulty": "hard", 
         "questions": ["Q1", "Q2"], "user_answers": ["A1", "Wrong"], 
         "correct_answers": ["A1", "A2"]},
        
        # Machine Learning - Moderate performance
        {"student_id": STUDENT_ID, "topic": "Machine Learning", "difficulty": "easy", 
         "questions": ["Q1", "Q2", "Q3"], "user_answers": ["A1", "A2", "Wrong"], 
         "correct_answers": ["A1", "A2", "A3"]},
        {"student_id": STUDENT_ID, "topic": "Machine Learning", "difficulty": "medium", 
         "questions": ["Q1", "Q2", "Q3"], "user_answers": ["A1", "Wrong", "A3"], 
         "correct_answers": ["A1", "A2", "A3"]},
        
        # Data Structures - Weak performance
        {"student_id": STUDENT_ID, "topic": "Data Structures", "difficulty": "easy", 
         "questions": ["Q1", "Q2", "Q3"], "user_answers": ["Wrong", "A2", "Wrong"], 
         "correct_answers": ["A1", "A2", "A3"]},
        {"student_id": STUDENT_ID, "topic": "Data Structures", "difficulty": "medium", 
         "questions": ["Q1", "Q2"], "user_answers": ["Wrong", "Wrong"], 
         "correct_answers": ["A1", "A2"]},
    ]
    
    for i, attempt in enumerate(attempts, 1):
        response = requests.post(f"{API_URL}/progress/record", json=attempt)
        if response.status_code == 200:
            result = response.json()
            print(f"  ✓ Attempt {i}/{len(attempts)}: {attempt['topic']} ({attempt['difficulty']}) - {result['accuracy']}%")
        else:
            print(f"  ✗ Failed attempt {i}: {response.status_code}")
        time.sleep(0.2)  # Small delay between requests
    
    print(f"\n✅ Created {len(attempts)} quiz attempts")

def test_analytics():
    """Test the analytics endpoint"""
    print(f"\n📊 Fetching analytics for {STUDENT_ID}...")
    
    response = requests.get(f"{API_URL}/progress/analytics/{STUDENT_ID}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ Analytics Retrieved Successfully!\n")
        print(json.dumps(data, indent=2))
        return True
    else:
        print(f"\n❌ Failed to retrieve analytics: {response.status_code}")
        print(response.text)
        return False

def open_dashboard():
    """Open the progress dashboard in browser"""
    print("\n🌐 Opening Progress Dashboard in browser...")
    dashboard_url = "http://localhost:8000/../frontend/test-progress.html"
    # Use file path for local testing
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.join(current_dir, "..", "..", "frontend", "test-progress.html")
    
    if os.path.exists(test_file):
        webbrowser.open(f'file://{os.path.abspath(test_file)}')
        print("✓ Dashboard opened in browser")
    else:
        print(f"✗ Test file not found: {test_file}")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Progress Dashboard Test Suite")
    print("=" * 60)
    
    # Step 1: Create sample data
    create_sample_data()
    
    # Step 2: Test analytics
    success = test_analytics()
    
    # Step 3: Open dashboard
    if success:
        open_dashboard()
        print("\n" + "=" * 60)
        print("✅ Test Complete!")
        print("💡 The dashboard should now be open in your browser")
        print("📝 Enter 'student_123' and click 'Load Dashboard'")
        print("=" * 60)
