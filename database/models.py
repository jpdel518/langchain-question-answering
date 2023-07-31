from sqlalchemy import Column, Integer, String, DateTime
from .database import Base


class Transcription(Base):
    __tablename__ = "transcriptions"
    transcription_id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True, nullable=False)
    text = Column(String, nullable=False)
    start = Column(String, nullable=False)
