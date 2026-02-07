from pydantic import BaseModel, Field
from typing import List

class Reflection(BaseModel):
    missing :str = Field(description="What is missing")
    superfluous: str = Field(description="What is unnecessary or extra")

class AnswerQuestion(BaseModel):
    answer: str = Field(description='The 250 word detailed answer to the question')
    reflection: Reflection = Field(description='Reflection on what is missing or unnecessary in the answer')
    search_queries: List[str] = Field(description='1-3 recommended search queries for further research')

class ReflectionFromAnswer(AnswerQuestion):
    """Revise your original answer to your question."""
    refrences: List[str] = Field(
        description="Citations motivating your updated answer."
        )
