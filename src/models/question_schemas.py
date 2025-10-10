from typing import List
from pydantic import BaseModel,Field,field_validator

class MCQQuestion(BaseModel):

    question: str = Field(description="The question text")

    options: List[str] = Field(description="List of 4 options")

    correct_answer: str = Field(description="The correct answer from the options")

    @field_validator('question', mode='before')
    @classmethod
    def clean_question(cls, v):
        if isinstance(v, dict):
            return v.get('description', str(v))
        if v is None:
            raise ValueError("Question cannot be None")
        return str(v).strip()
    

class FillBlankQuestion(BaseModel):

    question: str = Field(description="The question text with '___' for the blank")

    answer : str = Field(description="The correct word or phrase for the blank")

    @field_validator('question', mode='before')
    @classmethod
    def clean_question(cls, v):
        if isinstance(v, dict):
            return v.get('description', str(v))
        if v is None:
            raise ValueError("Question cannot be None")
        return str(v).strip()