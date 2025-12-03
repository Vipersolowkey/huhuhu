from sqlalchemy.orm import Session
from models import ExamMatrixItem
from schemas import MatrixUpsert
from uuid import uuid4


def upsert_matrix(db: Session, exam_id: str, data: MatrixUpsert):
    # Xóa matrix cũ
    db.query(ExamMatrixItem).filter(ExamMatrixItem.exam_id == exam_id).delete()

    # Insert matrix mới
    for item in data.items:
        db_item = ExamMatrixItem(
            id=str(uuid4()),
            exam_id=exam_id,
            **item.dict()
        )
        db.add(db_item)

    db.commit()


def get_matrix(db: Session, exam_id: str):
    return db.query(ExamMatrixItem).filter(ExamMatrixItem.exam_id == exam_id).all()
