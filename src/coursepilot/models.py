from typing import Literal
from pydantic import BaseModel, Field


class ParsedSection(BaseModel):
    title: str
    text: str
    location: int = 1


class DocumentChunk(BaseModel):
    id: str
    text: str
    document_id: str
    filename: str
    document_type: str
    section: str
    section_index: int
    location: int


class RetrievedChunk(DocumentChunk):
    distance: float | None = None


class QuizQuestion(BaseModel):
    id: str
    question_type: Literal["multiple_choice", "short_answer"]
    knowledge_point: str = Field(min_length=1)
    prompt: str
    options: list[str] = Field(default_factory=list)
    correct_answer: str
    explanation: str


class QuizAttempt(BaseModel):
    question_id: str
    knowledge_point: str
    user_answer: str
    is_correct: bool
    score: float = Field(ge=0, le=100)
    feedback: str = ""


class KnowledgePointMastery(BaseModel):
    knowledge_point: str
    probability: float
    attempt_count: int
    last_correct: bool | None = None
