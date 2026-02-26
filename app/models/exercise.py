from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from app.database.db import Base
from datetime import datetime

class Exercise(Base):
    __tablename__ = "exercise"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    exercise_type = Column(String, nullable=False)
    duration_minutes = Column(Float)
    calories_burned = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)