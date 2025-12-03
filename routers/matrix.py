from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from crud.matrix import upsert_matrix, get_matrix
from schemas import MatrixUpsert
from services.validate_matrix import validate_matrix

router = APIRouter(prefix="/matrix")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.put("/{exam_id}")
def update_matrix_api(exam_id: str, payload: MatrixUpsert, db: Session = Depends(get_db)):
    upsert_matrix(db, exam_id, payload)
    return {"status": "updated", "items": get_matrix(db, exam_id)}


@router.get("/{exam_id}")
def get_matrix_api(exam_id: str, db: Session = Depends(get_db)):
    return get_matrix(db, exam_id)


@router.post("/{exam_id}/validate")
def validate_matrix_api(exam_id: str, db: Session = Depends(get_db)):
    return validate_matrix(db, exam_id)
