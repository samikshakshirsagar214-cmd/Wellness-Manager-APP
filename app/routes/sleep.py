from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.sleep import Sleep
from app.schemas.sleep import SleepCreate, SleepOut
from app.core.deps import get_current_user
from app.models.user import User
from typing import List

router = APIRouter(prefix="/sleep", tags=["Sleep"])


def calculate_sleep_quality(hours: float) -> str:
    if hours < 6:
        return "Poor"
    elif hours < 7.5:
        return "Average"
    else:
        return "Good"


@router.post("/", response_model=SleepOut)
def add_sleep(
    sleep: SleepCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if sleep.wake_time <= sleep.sleep_time:
        raise HTTPException(
            status_code=400,
            detail="Wake time must be after sleep time"
        )

    duration = (sleep.wake_time - sleep.sleep_time).total_seconds() / 3600
    quality = calculate_sleep_quality(duration)

    sleep_record = Sleep(
        user_id=current_user.id,
        sleep_time=sleep.sleep_time,
        wake_time=sleep.wake_time,
        duration_hours=round(duration, 2),
        sleep_quality=quality
    )

    db.add(sleep_record)
    db.commit()
    db.refresh(sleep_record)

    return sleep_record









@router.get("/", response_model=List[dict])
def get_sleep_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sleep_data = (
        db.query(Sleep)
        .filter(Sleep.user_id == current_user.id)
        .order_by(Sleep.created_at.asc())
        .all()
    )

    return [
        {
            "id": s.id,
            "duration_hours": s.duration_hours,
            "created_at": s.created_at
        }
        for s in sleep_data
    ]