import json
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv

import schemas
import controller

from database import models
from database.database import SessionLocal, engine

load_dotenv()

# エンジンを元にデータベースの作成
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.post("/transcript")
async def transcript(model: schemas.CreatingTranscription, db: Session = Depends(get_db)):
    controller.transcribe_from_youtube(model, db)
    return {"message": "success"}


@app.get("/transcript")
async def transcript(db: Session = Depends(get_db)):
    return controller.get_distinct_transcriptions(db)


@app.post("/question")
async def question(model: schemas.AskingTranscription, db: Session = Depends(get_db)):
    answer = controller.generate_question_answer(model, db)
    return {"message": "success", "answer": answer}
