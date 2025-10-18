"""
Test AI Feedback Generation Service
Run: python -m src.services.test_ai_feedback
"""
import asyncio
import requests
import json

API_URL = "http://localhost:8000"
STUDENT_ID = "student_123"

async def test_feedback_service():
    """Test the feedback service directly"""
    from src.services.feedback_service import FeedbackGenerator
    
    print("🤖 Testing AI Feedback Generator directly...\n")
    
    generator = FeedbackGenerator()
    
    # Test strength feedback
    print("1️⃣ Generating Strength Feedback:")
    strength = await generator.generate_strength_feedback("Python Programming", 92.5, 5)
    print(f"   {strength}\n")
    
    # Test weakness feedback
    print("2️⃣ Generating Weakness Feedback:")
    weakness = await generator.generate_weakness_feedback("Data Structures", 45.0, 3)
    print(f"   {weakness}\n")
    
    # Test overall insight
    print("3️⃣ Generating Overall Insight:")
    topics = [
        {"topic": "Python", "accuracy": 92.5},
        {"topic": "ML", "accuracy": 78.0}
    ]
    insight = await generator.generate_overall_insight(85.0, 8, topics)
    print(f"   {insight}\n")
    
    return True

def create_test_data():
    """Create diverse quiz attempts"""
    print("📝 Creating sample data...")
    
    attempts = [
        {"student_id": STUDENT_ID, "topic": "Python", "difficulty": "easy", 
         "questions": ["Q1", "Q2", "Q3"], "user_answers": ["A1", "A2", "A3"], 
         "correct_answers": ["A1", "A2", "A3"]},
        {"student_id": STUDENT_ID, "topic": "Python", "difficulty": "medium", 
         "questions": ["Q1", "Q2"], "user_answers": ["A1", "A2"], 
         "correct_answers": ["A1", "A2"]},
        {"student_id": STUDENT_ID, "topic": "Algorithms", "difficulty": "hard", 
         "questions": ["Q1", "Q2", "Q3", "Q4"], "user_answers": ["Wrong", "A2", "Wrong", "A4"], 
         "correct_answers": ["A1", "A2", "A3", "A4"]},
    ]
    
    for attempt in attempts:
        requests.post(f"{API_URL}/progress/record", json=attempt)
    
    print(f"✅ Created {len(attempts)} attempts\n")

def test_ai_analytics_endpoint():
    """Test the /ai endpoint"""
    print("🌐 Testing AI Analytics Endpoint...")
    
    response = requests.get(f"{API_URL}/progress/analytics/{STUDENT_ID}/ai")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ AI Analytics Retrieved!\n")
        print(f"📊 Overall Accuracy: {data['overall_accuracy']}%")
        print(f"💪 Strongest Topic: {data['strongest_topic']}")
        print(f"📚 Weakest Topic: {data['weakest_topic']}\n")
        
        print("✨ AI-Generated Strength Feedback:")
        print(f"   {data.get('ai_strength_feedback', 'N/A')}\n")
        
        print("🎯 AI-Generated Weakness Feedback:")
        print(f"   {data.get('ai_weakness_feedback', 'N/A')}\n")
        
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return False

def compare_endpoints():
    """Compare regular vs AI endpoint"""
    print("🔄 Comparing Regular vs AI Endpoints...\n")
    
    # Regular endpoint
    regular = requests.get(f"{API_URL}/progress/analytics/{STUDENT_ID}")
    regular_data = regular.json() if regular.status_code == 200 else {}
    
    # AI endpoint
    ai = requests.get(f"{API_URL}/progress/analytics/{STUDENT_ID}/ai")
    ai_data = ai.json() if ai.status_code == 200 else {}
    
    print("Regular Endpoint:")
    print(f"  - Has AI feedback: {'ai_strength_feedback' in regular_data}")
    
    print("\nAI Endpoint:")
    print(f"  - Has AI feedback: {'ai_strength_feedback' in ai_data}")
    print(f"  - Strength feedback length: {len(ai_data.get('ai_strength_feedback', ''))} chars")
    print(f"  - Weakness feedback length: {len(ai_data.get('ai_weakness_feedback', ''))} chars")

async def main():
    print("=" * 70)
    print("🧪 AI Feedback Generation Test Suite")
    print("=" * 70 + "\n")
    
    # Test 1: Direct feedback service
    await test_feedback_service()
    
    print("=" * 70 + "\n")
    
    # Test 2: Create data
    create_test_data()
    
    # Test 3: API endpoint
    success = test_ai_analytics_endpoint()
    
    # Test 4: Compare endpoints
    compare_endpoints()
    
    if success:
        print("\n" + "=" * 70)
        print("✅ All Tests Passed!")
        print("\n💡 Open frontend and click 'My Progress' to see AI feedback")
        print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
