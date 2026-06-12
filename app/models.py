from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String, nullable=False)
    title = Column(String, nullable=True)
    provider = Column(String, nullable=False, default="ace_step")
    audio_path = Column(String, nullable=False)
    duration = Column(Float, nullable=True)
    created_at = Column(String, nullable=True)