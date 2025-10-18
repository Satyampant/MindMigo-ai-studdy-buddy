"""
Gamification Service - Business logic for XP, streaks, and badges
"""
from sqlalchemy.orm import Session
from src.database.models import StudentGamification, StudentBadge, XPTransaction
from src.config.gamification_config import XP_REWARDS, get_level_from_xp, check_badge_eligibility
from datetime import datetime, timedelta

class GamificationService:
    """Service for managing student gamification features"""
    
    def get_or_create_profile(self, db: Session, student_id: str) -> StudentGamification:
        student = db.query(StudentGamification).filter_by(student_id=student_id).first()
        if not student:
            student = StudentGamification(student_id=student_id, total_xp=0, level=1, current_streak=0, longest_streak=0)
            db.add(student)
            db.commit()
        return student
    
    def award_xp(self, db: Session, student_id: str, activity_type: str, description: str = None) -> dict:
        xp_amount = XP_REWARDS.get(activity_type, 0)
        student = self.get_or_create_profile(db, student_id)
        student.total_xp += xp_amount
        old_level = student.level
        student.level = get_level_from_xp(student.total_xp)
        transaction = XPTransaction(student_id=student_id, xp_amount=xp_amount, activity_type=activity_type, description=description or f"{activity_type.replace('_', ' ').title()}")
        db.add(transaction)
        db.commit()
        db.refresh(student)
        return {"xp_awarded": xp_amount, "total_xp": student.total_xp, "level": student.level, "level_up": student.level > old_level}
    
    def update_streak(self, db: Session, student_id: str) -> dict:
        student = self.get_or_create_profile(db, student_id)
        today = datetime.utcnow().date()
        last_date = student.last_activity_date.date() if student.last_activity_date else None
        if last_date == today:
            return {"current_streak": student.current_streak, "longest_streak": student.longest_streak, "streak_status": "already_counted"}
        elif last_date == today - timedelta(days=1):
            student.current_streak += 1
            student.longest_streak = max(student.longest_streak, student.current_streak)
            student.last_activity_date = datetime.utcnow()
            streak_status = "continued"
        else:
            student.current_streak = 1
            student.last_activity_date = datetime.utcnow()
            streak_status = "reset"
        db.commit()
        return {"current_streak": student.current_streak, "longest_streak": student.longest_streak, "streak_status": streak_status}
    
    def check_and_award_badges(self, db: Session, student_id: str) -> dict:
        student = db.query(StudentGamification).filter_by(student_id=student_id).first()
        if not student:
            return {"new_badges": [], "total_badges": 0}
        existing_badges = {badge.badge_id for badge in student.badges}
        stats = self._get_student_stats(db, student_id)
        eligible_badges = check_badge_eligibility(stats)
        new_badges = [badge_id for badge_id in eligible_badges if badge_id not in existing_badges]
        for badge_id in new_badges:
            db.add(StudentBadge(student_id=student_id, badge_id=badge_id, badge_type="achievement"))
        db.commit()
        return {"new_badges": new_badges, "total_badges": len(eligible_badges)}
    
    def get_student_gamification(self, db: Session, student_id: str) -> dict:
        student = self.get_or_create_profile(db, student_id)
        badges = [{"badge_id": b.badge_id, "badge_type": b.badge_type, "earned_date": b.earned_date.isoformat()} for b in student.badges]
        recent_transactions = [{"xp_amount": t.xp_amount, "activity_type": t.activity_type, "description": t.description, "timestamp": t.timestamp.isoformat()} for t in student.transactions[:10]]
        return {"student_id": student_id, "total_xp": student.total_xp, "level": student.level, "current_streak": student.current_streak, "longest_streak": student.longest_streak, "last_activity_date": student.last_activity_date.isoformat() if student.last_activity_date else None, "badges": badges, "recent_transactions": recent_transactions}
    
    def _get_student_stats(self, db: Session, student_id: str) -> dict:
        from src.database.models import StudentQuizAttempt, ChatMessageDB, Conversation
        student = db.query(StudentGamification).filter_by(student_id=student_id).first()
        if not student:
            return {"quizzes_completed": 0, "graphs_created": 0, "longest_streak": 0, "current_streak": 0, "total_xp": 0, "perfect_quizzes": 0, "level": 1, "chat_count": 0}
        quizzes = db.query(StudentQuizAttempt).filter_by(student_id=student_id).all()
        chats = db.query(ChatMessageDB).join(Conversation).filter(Conversation.student_id == student_id, ChatMessageDB.role == "student").count()
        perfect_quizzes = sum(1 for q in quizzes if q.correct_count == q.total_questions)
        graphs_created = sum(1 for t in student.transactions if t.activity_type == "graph_creation")
        return {"quizzes_completed": len(quizzes), "graphs_created": graphs_created, "longest_streak": student.longest_streak, "current_streak": student.current_streak, "total_xp": student.total_xp, "perfect_quizzes": perfect_quizzes, "level": student.level, "chat_count": chats}
