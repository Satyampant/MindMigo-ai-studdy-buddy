from sqlalchemy.orm import Session
from src.database.models import StudentQuizAttempt, StudentTopicPerformance
from src.models.progress_schemas import QuizAttemptRequest
from src.services.feedback_service import FeedbackGenerator
from src.services.gamification_service import GamificationService
from datetime import datetime, timedelta
import uuid

class ProgressService:
    def __init__(self):
        self.feedback_generator = FeedbackGenerator()
        self.gamification_service = GamificationService()

    def record_quiz_attempt(self, db: Session, attempt: QuizAttemptRequest) -> dict:
        correct_count = sum(1 for user, correct in zip(attempt.user_answers, attempt.correct_answers) if user.strip().lower() == correct.strip().lower())
        total = len(attempt.questions)
        accuracy = (correct_count / total * 100) if total > 0 else 0
        quiz_id = f"quiz_{uuid.uuid4().hex[:8]}"
        
        quiz_attempt = StudentQuizAttempt(
            quiz_id=quiz_id, student_id=attempt.student_id, topic=attempt.topic,
            difficulty=attempt.difficulty, questions=attempt.questions,
            answers=attempt.user_answers, correct_count=correct_count, total_questions=total
        )
        db.add(quiz_attempt)
        
        topic_perf = db.query(StudentTopicPerformance).filter_by(student_id=attempt.student_id, topic=attempt.topic).first()
        if not topic_perf:
            topic_perf = StudentTopicPerformance(student_id=attempt.student_id, topic=attempt.topic, difficulty_distribution={})
            db.add(topic_perf)
        
        topic_perf.total_attempts += 1
        topic_perf.correct_answers += correct_count
        topic_perf.last_attempted = datetime.utcnow()
        diff_dist = topic_perf.difficulty_distribution or {}
        diff_dist[attempt.difficulty] = diff_dist.get(attempt.difficulty, 0) + 1
        topic_perf.difficulty_distribution = diff_dist
        
        db.commit()
        
        return {"quiz_id": quiz_id, "accuracy": round(accuracy, 2), "correct_count": correct_count, "total_questions": total, "timestamp": quiz_attempt.timestamp}

    def get_student_analytics(self, db: Session, student_id: str) -> dict:
        attempts = db.query(StudentQuizAttempt).filter_by(student_id=student_id).all()
        if not attempts:
            return {"student_id": student_id, "overall_accuracy": 0, "total_attempts": 0, "topics": [], "weekly_trend": [], "strongest_topic": "N/A", "weakest_topic": "N/A", "difficulty_distribution": {}, "ai_strength_feedback": "Complete some quizzes to receive personalized feedback!", "ai_weakness_feedback": "Start your learning journey today!"}
        
        total_correct = sum(a.correct_count for a in attempts)
        total_questions = sum(a.total_questions for a in attempts)
        overall_accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0
        
        topics_data = db.query(StudentTopicPerformance).filter_by(student_id=student_id).all()
        topics = []
        for t in topics_data:
            total_q_for_topic = sum(a.total_questions for a in attempts if a.topic == t.topic)
            topic_accuracy = (t.correct_answers / total_q_for_topic * 100) if total_q_for_topic > 0 else 0
            topics.append({
                "topic": t.topic,
                "accuracy": round(topic_accuracy, 2),
                "total_attempts": t.total_attempts,
                "correct_answers": t.correct_answers,
                "total_questions": total_q_for_topic
            })
        
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        weekly_trend = []
        for i in range(7):
            day = datetime.utcnow() - timedelta(days=6-i)
            day_attempts = [a for a in attempts if a.timestamp.date() == day.date()]
            day_correct = sum(a.correct_count for a in day_attempts)
            day_total = sum(a.total_questions for a in day_attempts)
            day_accuracy = round((day_correct / day_total * 100) if day_total > 0 else 0, 2)
            weekly_trend.append({
                "date": day.strftime("%Y-%m-%d"),
                "accuracy": day_accuracy,
                "attempts": len(day_attempts)
            })
        
        strongest = max(topics, key=lambda x: x["accuracy"])["topic"] if topics else "N/A"
        weakest = min(topics, key=lambda x: x["accuracy"])["topic"] if topics else "N/A"
        
        diff_dist = {}
        for a in attempts:
            diff_dist[a.difficulty] = diff_dist.get(a.difficulty, 0) + 1
        
        return {
            "student_id": student_id,
            "overall_accuracy": round(overall_accuracy, 2),
            "total_attempts": len(attempts),
            "topics": topics,
            "weekly_trend": weekly_trend,
            "strongest_topic": strongest,
            "weakest_topic": weakest,
            "difficulty_distribution": diff_dist
        }

    async def get_student_analytics_with_ai_feedback(self, db: Session, student_id: str) -> dict:
        analytics = self.get_student_analytics(db, student_id)
        
        if analytics["total_attempts"] == 0:
            return {**analytics, "ai_strength_feedback": "Complete some quizzes to receive personalized feedback!", "ai_weakness_feedback": "Start your learning journey today!"}
        
        strongest_topic_data = next((t for t in analytics["topics"] if t["topic"] == analytics["strongest_topic"]), None)
        weakest_topic_data = next((t for t in analytics["topics"] if t["topic"] == analytics["weakest_topic"]), None)
        
        strength_feedback = await self.feedback_generator.generate_strength_feedback(
            analytics["strongest_topic"],
            strongest_topic_data["accuracy"] if strongest_topic_data else 0,
            strongest_topic_data["total_attempts"] if strongest_topic_data else 0
        )
        
        weakness_feedback = await self.feedback_generator.generate_weakness_feedback(
            analytics["weakest_topic"],
            weakest_topic_data["accuracy"] if weakest_topic_data else 0,
            weakest_topic_data["total_attempts"] if weakest_topic_data else 0
        )
        
        return {**analytics, "ai_strength_feedback": strength_feedback, "ai_weakness_feedback": weakness_feedback}
