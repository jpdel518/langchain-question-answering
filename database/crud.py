import json

from sqlalchemy.orm import Session
from sqlalchemy import distinct
from . import models
import schemas
import utils


# transcription作成
def create_transcription(db: Session, transcription: schemas.Transcription):
    db_data = models.Transcription(url=transcription.url, text=transcription.text, start=transcription.start)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


# transcription取得
def fetch_transcription(db: Session, url: str):
    return db.query(models.Transcription).\
        filter(models.Transcription.url == url).\
        all()


def distinct_transcription(db: Session):
    # return db.query(models.Transcription).\
    #     distinct(models.Transcription.url).\
    #     all()
    return db.query(distinct(models.Transcription.url)).all()
