from typing import List
from pydantic import BaseModel, Field, field_validator

class MCQQuestion(BaseModel):
    question: str = Field(..., description="The question text")
    options: List[str] = Field(..., description="List of 4 answer options")
    correct_option: str = Field(..., description="The correct answer from the option")

    @field_validator('question', mode='before')
    def clean_question(cls, v):
        if isinstance(v, dict):
            return v.get('description', str(v))
        return str(v)
    
    class FillBlankQuestion(BaseModel):
        question: str = Field(..., description="The question text with a blank")
        answer: str = Field(..., description="The correct answer to fill in the blank")

        @field_validator('question', mode='before')
        def clean_question(cls, v):
            if isinstance(v, dict):
                return v.get('description', str(v))
            return str(v)