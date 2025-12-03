from sqlalchemy import Column, String, Integer, Numeric, Enum, Boolean, JSON, ForeignKey
import enum
from uuid import uuid4
from database import Base

class ExamStatus(str, enum.Enum):
    draft = "draft"
    matrix_locked = "matrix_locked"
    generated = "generated"


class BloomLevel(str, enum.Enum):
    REMEMBER = "REMEMBER"
    UNDERSTAND = "UNDERSTAND"
    APPLY = "APPLY"
    ANALYZE = "ANALYZE"


class Difficulty(str, enum.Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class Exam(Base):
    __tablename__ = "exams"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(String)
    subject_id = Column(String)
    grade = Column(Integer)
    name = Column(String)
    description = Column(String)
    time_limit = Column(Integer)
    total_marks = Column(Numeric)
    status = Column(Enum(ExamStatus), default=ExamStatus.draft)
    created_by = Column(String)


class ExamMatrixItem(Base):
    __tablename__ = "exam_matrix_items"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    exam_id = Column(String, ForeignKey("exams.id", ondelete="CASCADE"))
    topic_id = Column(String)
    bloom_level = Column(Enum(BloomLevel))
    difficulty = Column(Enum(Difficulty), nullable=True)
    num_questions = Column(Integer)
    marks_per_question = Column(Numeric)
    notes = Column(String)


class Question(Base):
    __tablename__ = "questions"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    subject_id = Column(String)
    grade = Column(Integer)
    topic_id = Column(String)
    bloom_level = Column(Enum(BloomLevel))
    difficulty = Column(Enum(Difficulty), nullable=True)
    type = Column(String)
    content = Column(JSON)
    is_active = Column(Boolean, default=True)


class GeneratedExamQuestion(Base):
    __tablename__ = "generated_exam_questions"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    exam_id = Column(String)
    question_id = Column(String)
    matrix_item_id = Column(String)
    order_index = Column(Integer)
