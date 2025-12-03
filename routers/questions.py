from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Question
from schemas import QuestionCreate
from uuid import uuid4

router = APIRouter(prefix="/questions")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_question(payload: QuestionCreate, db: Session = Depends(get_db)):
    q = Question(id=str(uuid4()), **payload.dict())
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


@router.get("/")
def list_questions(db: Session = Depends(get_db)):
    return db.query(Question).all()


@router.get("/{question_id}")
def get_question(question_id: str, db: Session = Depends(get_db)):
    return db.query(Question).filter(Question.id == question_id).first()


@router.put("/{question_id}")
def update_question(question_id: str, payload: QuestionCreate, db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == question_id).first()
    for k, v in payload.dict().items():
        setattr(q, k, v)
    db.commit()
    return q


@router.delete("/{question_id}")
def delete_question(question_id: str, db: Session = Depends(get_db)):
    db.query(Question).filter(Question.id == question_id).delete()
    db.commit()
    return {"status": "deleted"}
