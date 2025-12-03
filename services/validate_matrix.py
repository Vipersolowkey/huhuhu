from sqlalchemy.orm import Session
from models import Question, Exam
from crud.matrix import get_matrix


def validate_matrix(db: Session, exam_id: str):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    items = get_matrix(db, exam_id)

    summary_items = []
    total_required = 0
    all_ok = True

    for item in items:
        query = db.query(Question).filter(
            Question.subject_id == exam.subject_id,
            Question.grade == exam.grade,
            Question.topic_id == item.topic_id,
            Question.bloom_level == item.bloom_level,
            Question.is_active == True
        )

        if item.difficulty:
            query = query.filter(Question.difficulty == item.difficulty)

        available = query.count()
        required = item.num_questions

        ok = available >= required
        if not ok:
            all_ok = False

        summary_items.append({
            "topic_id": item.topic_id,
            "bloom_level": item.bloom_level,
            "required": required,
            "available": available,
            "is_enough": ok
        })

        total_required += required

    return {
        "summary": {
            "total_required_questions": total_required,
            "is_enough": all_ok
        },
        "items": summary_items
    }
