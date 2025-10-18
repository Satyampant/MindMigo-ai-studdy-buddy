"""
Test script for integrated quiz submission with progress tracking
Run: python -m src.services.test_quiz_integration
"""
import requests
import json

API_URL = "http://localhost:8000"

def test_quiz_generation():
    """Test generating a quiz"""
    print("📝 Step 1: Generating a quiz...")
    
    quiz_request = {
        "topic": "Python Programming",
        "question_type": "Multiple Choice",
        "difficulty": "medium",
        "num_questions": 3
    }
    
    response = requests.post(f"{API_URL}/quiz/generate", json=quiz_request)
    
    if response.status_code == 200:
        quiz = response.json()
        print(f"✅ Quiz generated: {len(quiz['questions'])} questions")
        print(json.dumps(quiz, indent=2))
        return quiz, quiz_request
    else:
        print(f"❌ Failed: {response.status_code}")
        return None, None

def test_progress_recording(quiz, settings):
    """Test recording progress after quiz completion"""
    print("\n📊 Step 2: Recording quiz attempt...")
    
    # Simulate user answering all questions correctly
    progress_data = {
        "student_id": "student_123",
        "topic": settings["topic"],
        "difficulty": settings["difficulty"],
        "questions": [q["question"] for q in quiz["questions"]],
        "user_answers": [q["correct_answer"] for q in quiz["questions"]],
        "correct_answers": [q["correct_answer"] for q in quiz["questions"]]
    }
    
    response = requests.post(f"{API_URL}/progress/record", json=progress_data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Progress recorded:")
        print(f"   Quiz ID: {result['quiz_id']}")
        print(f"   Accuracy: {result['accuracy']}%")
        print(f"   Correct: {result['correct_count']}/{result['total_questions']}")
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return False

def test_analytics_retrieval():
    """Test retrieving analytics after recording"""
    print("\n📈 Step 3: Retrieving updated analytics...")
    
    response = requests.get(f"{API_URL}/progress/analytics/student_123")
    
    if response.status_code == 200:
        analytics = response.json()
        print(f"✅ Analytics retrieved:")
        print(f"   Overall Accuracy: {analytics['overall_accuracy']}%")
        print(f"   Total Attempts: {analytics['total_attempts']}")
        print(f"   Strongest Topic: {analytics['strongest_topic']}")
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Quiz Integration Test")
    print("=" * 60)
    
    # Test the full workflow
    quiz, settings = test_quiz_generation()
    
    if quiz:
        success = test_progress_recording(quiz, settings)
        
        if success:
            test_analytics_retrieval()
            
            print("\n" + "=" * 60)
            print("✅ Integration Test Complete!")
            print("\n💡 Next Steps:")
            print("1. Open frontend/index.html in browser")
            print("2. Navigate to 'Quiz Generator'")
            print("3. Generate and submit a quiz")
            print("4. Check 'My Progress' to see recorded data")
            print("=" * 60)
        else:
            print("\n❌ Integration test failed at progress recording")
    else:
        print("\n❌ Integration test failed at quiz generation")
