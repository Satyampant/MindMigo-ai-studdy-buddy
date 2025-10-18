from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class StudentQuizAttempt(Base):
    __tablename__ = "student_quiz_attempts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(String, nullable=False)
    student_id = Column(String, nullable=False, index=True)
    topic = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    questions = Column(JSON, nullable=False)
    answers = Column(JSON, nullable=False)
    correct_count = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)

class StudentTopicPerformance(Base):
    __tablename__ = "student_topic_performance"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, nullable=False, index=True)
    topic = Column(String, nullable=False)
    total_attempts = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    last_attempted = Column(DateTime, default=datetime.utcnow)
    difficulty_distribution = Column(JSON, default=dict)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String, primary_key=True)
    student_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    messages = relationship("ChatMessageDB", back_populates="conversation", cascade="all, delete-orphan")

class ChatMessageDB(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False, index=True)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    conversation = relationship("Conversation", back_populates="messages")

class StudentGamification(Base):
    __tablename__ = "student_gamification"
    student_id = Column(String, primary_key=True, index=True)
    total_xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(DateTime, nullable=True)
    badges = relationship("StudentBadge", back_populates="student", cascade="all, delete-orphan")
    transactions = relationship("XPTransaction", back_populates="student", cascade="all, delete-orphan")

class StudentBadge(Base):
    __tablename__ = "student_badges"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, ForeignKey("student_gamification.student_id"), nullable=False, index=True)
    badge_id = Column(String, nullable=False)
    earned_date = Column(DateTime, default=datetime.utcnow)
    badge_type = Column(String, nullable=False)
    student = relationship("StudentGamification", back_populates="badges")

class XPTransaction(Base):
    __tablename__ = "xp_transactions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, ForeignKey("student_gamification.student_id"), nullable=False, index=True)
    xp_amount = Column(Integer, nullable=False)
    activity_type = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    description = Column(String, nullable=True)
    student = relationship("StudentGamification", back_populates="transactions")
