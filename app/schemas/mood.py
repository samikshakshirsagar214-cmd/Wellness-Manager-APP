from pydantic import BaseModel

class MoodCreate(BaseModel):
    mood: str
    note: str | None = None