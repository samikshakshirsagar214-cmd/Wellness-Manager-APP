from pydantic import BaseModel
from datetime import datetime

class SleepCreate(BaseModel):
    sleep_time: datetime
    wake_time: datetime

class SleepOut(BaseModel):
    id: int
    sleep_time: datetime
    wake_time: datetime
    duration_hours: float
    sleep_quality: str
    created_at: datetime

    class Config:
        from_attributes = True