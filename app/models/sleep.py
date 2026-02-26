from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Sleep(Base):
    __tablename__ = "sleep"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    sleep_time = Column(DateTime, nullable=False)
    wake_time = Column(DateTime, nullable=False)

    duration_hours = Column(Float, nullable=False)
    sleep_quality = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sleep_records")