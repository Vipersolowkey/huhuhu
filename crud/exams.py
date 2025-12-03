from sqlalchemy.orm import Session
from models import Exam, ExamStatus
from schemas import ExamCreate


def create_exam(db: Session, data: ExamCreate):
    exam = Exam(**data.dict())
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


def get_exam(db: Session, exam_id: str):
    return db.query(Exam).filter(Exam.id == exam_id).first()


def lock_exam(db: Session, exam_id: str):
    exam = get_exam(db, exam_id)
    exam.status = ExamStatus.matrix_locked
    db.commit()
    db.refresh(exam)
    return exam
