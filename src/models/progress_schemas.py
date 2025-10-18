from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime

class QuizAttemptRequest(BaseModel):
    """Request schema for recording a quiz attempt."""
    student_id: str = Field(..., description="Unique identifier for the student")
    topic: str = Field(..., description="Quiz topic (e.g., 'Python', 'Machine Learning')")
    difficulty: str = Field(..., description="Difficulty level: 'easy', 'medium', or 'hard'")
    questions: List[str] = Field(..., description="List of question texts")
    user_answers: List[str] = Field(..., description="List of user's answers")
    correct_answers: List[str] = Field(..., description="List of correct answers")

class QuizAttemptResponse(BaseModel):
    """Response schema after recording quiz attempt."""
    quiz_id: str
    accuracy: float
    correct_count: int
    total_questions: int
    timestamp: datetime

class TopicPerformance(BaseModel):
    """Performance metrics for a single topic."""
    topic: str
    accuracy: float
    total_attempts: int
    correct_answers: int
    total_questions: int

class WeeklyTrend(BaseModel):
    """Weekly accuracy trend data point."""
    date: str
    accuracy: float
    attempts: int

class AnalyticsResponse(BaseModel):
    """Response schema for student analytics."""
    student_id: str
    overall_accuracy: float
    total_attempts: int
    topics: List[TopicPerformance]
    weekly_trend: List[WeeklyTrend]
    strongest_topic: str
    weakest_topic: str
    difficulty_distribution: Dict[str, int]
    ai_strength_feedback: str = ""
    ai_weakness_feedback: str = ""
