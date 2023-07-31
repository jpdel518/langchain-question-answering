import datetime
from pydantic import BaseModel


class CreatingTranscription(BaseModel):
    url: str


class AskingTranscription(CreatingTranscription):
    question: str


class Transcription(CreatingTranscription):
    text: str
    start: str

    class Config:
        orm_mode = True
