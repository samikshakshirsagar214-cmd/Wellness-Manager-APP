from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database.db import Base
from datetime import datetime

class Mood(Base):
    __tablename__ = "mood"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    mood = Column(String, nullable=False)  # Happy, Sad, Calm, etc
    note = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)