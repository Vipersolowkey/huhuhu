from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import ExamCreate
from crud.exams import create_exam, lock_exam
from services.validate_matrix import validate_matrix
from services.generate_exam import generate_exam

router = APIRouter(prefix="/exams")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_exam_api(payload: ExamCreate, db: Session = Depends(get_db)):
    return create_exam(db, payload)


@router.post("/{exam_id}/lock")
def lock_matrix_api(exam_id: str, db: Session = Depends(get_db)):
    validation = validate_matrix(db, exam_id)

    if not validation["summary"]["is_enough"]:
        raise HTTPException(status_code=400, detail="Matrix insufficient")

    return lock_exam(db, exam_id)


@router.post("/{exam_id}/generate")
def generate_exam_api(exam_id: str, db: Session = Depends(get_db)):
    generated = generate_exam(db, exam_id)
    return {"generated_count": len(generated)}
