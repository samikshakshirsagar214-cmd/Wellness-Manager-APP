from pydantic import BaseModel

class ExerciseCreate(BaseModel):
    exercise_type: str
    duration_minutes: float
    calories_burned: float