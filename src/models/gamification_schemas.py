"""
Pydantic schemas for gamification API responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class BadgeResponse(BaseModel):
    """Schema for individual badge"""
    badge_id: str = Field(..., description="Unique badge identifier")
    badge_name: str = Field(..., description="Display name of badge")
    badge_type: str = Field(..., description="Type of badge (e.g., achievement)")
    description: str = Field(..., description="Badge description")
    earned_date: str = Field(..., description="ISO format date when badge was earned")


class XPTransactionResponse(BaseModel):
    """Schema for XP transaction"""
    xp_amount: int
    activity_type: str
    description: str
    timestamp: str


class GamificationProfile(BaseModel):
    """Complete gamification profile for a student"""
    student_id: str
    total_xp: int
    level: int
    current_streak: int
    longest_streak: int
    last_activity_date: Optional[str] = None
    badges: List[BadgeResponse]
    recent_transactions: List[XPTransactionResponse]
    xp_for_next_level: int = Field(..., description="XP needed to reach next level")
    level_progress_percentage: float = Field(..., description="Progress toward next level (0-100)")


class LeaderboardEntry(BaseModel):
    """Schema for leaderboard entry"""
    rank: int
    student_id: str
    display_name: str = Field(..., description="Anonymized or actual name based on privacy settings")
    total_xp: int
    level: int
    badge_count: int
    is_current_user: bool = Field(default=False, description="Highlight current user")


class LeaderboardResponse(BaseModel):
    """Schema for leaderboard response"""
    entries: List[LeaderboardEntry]
    total_students: int
    current_user_rank: Optional[int] = None
