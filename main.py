from fastapi import FastAPI
from routers import exams, matrix, questions
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(exams.router)
app.include_router(matrix.router)
app.include_router(questions.router)
