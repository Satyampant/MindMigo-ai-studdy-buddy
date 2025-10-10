from pydantic import BaseModel, Field
from typing import List, Optional

# --- Quiz Schemas ---

class QuizSettings(BaseModel):
    """Request schema for generating a quiz."""
    topic: str = Field(..., description="The topic for the quiz, e.g., 'Python programming'.")
    question_type: str = Field(..., description="The type of question: 'Multiple Choice' or 'Fill in the blank'.")
    difficulty: str = Field(..., description="The difficulty level: 'easy', 'medium', or 'hard'.")
    num_questions: int = Field(5, description="The number of questions to generate (max 10).", ge=1, le=10)

class QuizQuestion(BaseModel):
    """Structure for a single question in the quiz response."""
    type: str = Field(..., description="Type of question: 'MCQ' or 'Fill in the blank'.")
    question: str = Field(..., description="The question text.")
    options: List[str] = Field(default_factory=list, description="List of options for MCQ, empty for Fill in the blank.")
    correct_answer: str = Field(..., description="The correct answer.")

class QuizResponse(BaseModel):
    """Response schema for a generated quiz."""
    questions: List[QuizQuestion]

# --- Knowledge Graph Schemas ---

class KnowledgeGraphRequest(BaseModel):
    """Request schema for generating a knowledge graph."""
    # User can provide text OR a topic. Text is for content analysis, topic is for content generation first.
    text: Optional[str] = Field(None, description="The text content to generate the knowledge graph over. If provided, overrides 'topic'.")
    topic: Optional[str] = Field(None, description="The topic to generate content for first, then create a knowledge graph from the content.")

class KnowledgeGraphResponse(BaseModel):
    """Response schema for a generated knowledge graph."""
    html_content: str = Field(..., description="Base64 encoded HTML content of the PyVis knowledge graph.")
    encoding: str = Field(default="base64", description="Encoding format of html_content")

# --- Daily Problem Schemas ---

class DailyProblemResponse(BaseModel):
    """Response schema for the daily problem."""
    question_type: str = Field("MCQ", description="The type of question.")
    topic: str = Field(..., description="The topic of the daily question.")
    difficulty: str = Field("hard", description="The difficulty of the daily question.")
    question: str
    options: List[str]
    correct_answer: str