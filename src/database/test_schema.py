from src.database.database import init_db, engine
from src.database.models import StudentQuizAttempt, StudentTopicPerformance
from datetime import datetime

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("✓ Database schema created successfully!")
    
    # Test insert
    from sqlalchemy.orm import Session
    with Session(engine) as session:
        test_attempt = StudentQuizAttempt(
            quiz_id="quiz_001", student_id="student_001", topic="Python", 
            difficulty="medium", questions=["Q1", "Q2"], answers=["A1", "A2"],
            correct_count=2, total_questions=2
        )
        session.add(test_attempt)
        session.commit()
        print(f"✓ Test record created with ID: {test_attempt.id}")
