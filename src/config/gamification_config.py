"""
Gamification Configuration - XP Rewards, Badge Definitions, and Level System
"""

# XP Rewards for different activities
XP_REWARDS = {
    "quiz_completion": 50,
    "graph_creation": 100,
    "daily_login": 10,
    "perfect_quiz": 100,
    "daily_problem": 75,
    "chat_interaction": 5,
    "streak_milestone": 50,
}

# Badge Definitions with eligibility criteria
BADGE_DEFINITIONS = {
    "QUIZ_MASTER": {"name": "Quiz Master", "description": "Complete 50 quizzes", "criteria": {"quizzes_completed": 50}},
    "QUIZ_LEGEND": {"name": "Quiz Legend", "description": "Complete 100 quizzes", "criteria": {"quizzes_completed": 100}},
    "GRAPH_GURU": {"name": "Graph Guru", "description": "Create 20 knowledge graphs", "criteria": {"graphs_created": 20}},
    "GRAPH_MASTER": {"name": "Graph Master", "description": "Create 50 knowledge graphs", "criteria": {"graphs_created": 50}},
    "CONSISTENCY_CHAMP": {"name": "Consistency Champ", "description": "Maintain a 30-day streak", "criteria": {"longest_streak": 30}},
    "STREAK_WARRIOR": {"name": "Streak Warrior", "description": "Maintain a 7-day streak", "criteria": {"current_streak": 7}},
    "PERFECTIONIST": {"name": "Perfectionist", "description": "Score 100% on 10 quizzes", "criteria": {"perfect_quizzes": 10}},
    "KNOWLEDGE_SEEKER": {"name": "Knowledge Seeker", "description": "Earn 1000 total XP", "criteria": {"total_xp": 1000}},
    "ELITE_LEARNER": {"name": "Elite Learner", "description": "Reach Level 10", "criteria": {"level": 10}},
    "CHAT_ENTHUSIAST": {"name": "Chat Enthusiast", "description": "Have 50 chat interactions", "criteria": {"chat_count": 50}},
}

# Level Thresholds (XP required for each level)
LEVEL_THRESHOLDS = [
    0,      # Level 1: 0-99 XP
    100,    # Level 2: 100-299 XP
    300,    # Level 3: 300-599 XP
    600,    # Level 4: 600-999 XP
    1000,   # Level 5: 1000-1499 XP
    1500,   # Level 6: 1500-2099 XP
    2100,   # Level 7: 2100-2799 XP
    2800,   # Level 8: 2800-3599 XP
    3600,   # Level 9: 3600-4499 XP
    4500,   # Level 10: 4500-5499 XP
    5500,   # Level 11: 5500-6599 XP
    6600,   # Level 12: 6600-7799 XP
    7800,   # Level 13: 7800-9099 XP
    9100,   # Level 14: 9100-10499 XP
    10500,  # Level 15: 10500+ XP
]


def get_level_from_xp(xp: int) -> int:
    """Calculate level based on total XP using LEVEL_THRESHOLDS"""
    for i in range(len(LEVEL_THRESHOLDS) - 1, -1, -1):
        if xp >= LEVEL_THRESHOLDS[i]:
            return i + 1
    return 1


def check_badge_eligibility(stats: dict) -> list[str]:
    """Check which badges the student is eligible for based on their stats"""
    return [badge_id for badge_id, badge in BADGE_DEFINITIONS.items() 
            if all(stats.get(key, 0) >= value for key, value in badge["criteria"].items())]


def get_xp_for_next_level(current_xp: int) -> int:
    """Calculate XP needed to reach the next level"""
    current_level = get_level_from_xp(current_xp)
    return LEVEL_THRESHOLDS[current_level] - current_xp if current_level < len(LEVEL_THRESHOLDS) else 0


def get_level_progress_percentage(current_xp: int) -> float:
    """Calculate percentage progress toward next level"""
    current_level = get_level_from_xp(current_xp)
    if current_level >= len(LEVEL_THRESHOLDS):
        return 100.0
    level_start = LEVEL_THRESHOLDS[current_level - 1]
    level_end = LEVEL_THRESHOLDS[current_level]
    return round(((current_xp - level_start) / (level_end - level_start)) * 100, 2)
