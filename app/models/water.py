from sqlalchemy import Column, Integer, DateTime, ForeignKey
from app.database.db import Base
from datetime import datetime

class Water(Base):
    __tablename__ = "water"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount_ml = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)