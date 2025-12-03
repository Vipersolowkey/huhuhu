from pydantic import BaseModel
from typing import Optional, List
from models import BloomLevel, Difficulty

class ExamCreate(BaseModel):
    tenant_id: str
    subject_id: str
    grade: int
    name: str
    description: Optional[str]
    time_limit: int
    total_marks: float
    created_by: str


class MatrixItem(BaseModel):
    topic_id: str
    bloom_level: BloomLevel
    difficulty: Optional[Difficulty]
    num_questions: int
    marks_per_question: float
    notes: Optional[str] = None


class MatrixUpsert(BaseModel):
    items: List[MatrixItem]


class QuestionCreate(BaseModel):
    subject_id: str
    grade: int
    topic_id: str
    bloom_level: BloomLevel
    difficulty: Optional[Difficulty]
    type: str
    content: dict
