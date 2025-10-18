"""Script to initialize test data for gamification system"""
from src.database.database import get_db
from src.services.gamification_service import GamificationService
import random

def initialize_test_data():
    db = next(get_db())
    service = GamificationService()
    test_students = [f"student_{i:03d}" for i in range(1, 11)]
    activities = ["quiz_completion", "graph_creation", "daily_login", "perfect_quiz"]
    
    for student_id in test_students:
        for _ in range(random.randint(5, 20)):
            activity = random.choice(activities)
            service.award_xp(db, student_id, activity)
            service.update_streak(db, student_id)
        service.check_and_award_badges(db, student_id)
    
    print(f"✅ Initialized gamification data for {len(test_students)} students")

if __name__ == "__main__":
    initialize_test_data()
