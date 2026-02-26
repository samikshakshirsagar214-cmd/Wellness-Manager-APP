from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.core.deps import get_current_user
from app.models.mood import Mood
from app.schemas.mood import MoodCreate
from typing import List
from app.models.user import User

router = APIRouter(prefix="/mood", tags=["Mood"])

@router.post("/")
def add_mood(data: MoodCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    mood = Mood(user_id=user.id, mood=data.mood, note=data.note)
    db.add(mood)
    db.commit()
    db.refresh(mood)
    return mood




@router.get("/", response_model=List[dict])
def get_mood_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    mood_data = (
        db.query(Mood)
        .filter(Mood.user_id == current_user.id)
        .order_by(Mood.created_at.asc())
        .all()
    )

    return [
        {
            "id": m.id,
            "mood": m.mood,              # text (Happy, Sad, etc.)
            "note": m.note,
            "created_at": m.created_at
        }
        for m in mood_data
    ]