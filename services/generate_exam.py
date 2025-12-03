import random
from sqlalchemy.orm import Session
from models import Exam, ExamMatrixItem, Question, GeneratedExamQuestion
from uuid import uuid4

def generate_exam(db: Session, exam_id: str):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    matrix_items = db.query(ExamMatrixItem).filter(ExamMatrixItem.exam_id == exam_id).all()

    generated_questions = []
    order_index = 1

    for item in matrix_items:
        query = db.query(Question).filter(
            Question.subject_id == exam.subject_id,
            Question.grade == exam.grade,
            Question.topic_id == item.topic_id,
            Question.bloom_level == item.bloom_level,
            Question.is_active == True
        )

        if item.difficulty:
            query = query.filter(Question.difficulty == item.difficulty)

        candidates = query.all()
        chosen = random.sample(candidates, item.num_questions)

        for q in chosen:
            new_row = GeneratedExamQuestion(
                id=str(uuid4()),
                exam_id=exam_id,
                question_id=q.id,
                matrix_item_id=item.id,
                order_index=order_index
            )
            db.add(new_row)
            generated_questions.append(new_row)
            order_index += 1

    db.commit()
    return generated_questions
