from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.core.deps import get_current_user
from app.models.exercise import Exercise
from app.schemas.exercise import ExerciseCreate

router = APIRouter(prefix="/exercise", tags=["Exercise"])

@router.post("/")
def add_exercise(data: ExerciseCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    exercise = Exercise(
        user_id=user.id,
        exercise_type=data.exercise_type,
        duration_minutes=data.duration_minutes,
        calories_burned=data.calories_burned
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise

@router.get("/")
def get_exercise(db: Session = Depends(get_db),
                 current_exercise: Exercise = Depends(get_current_user)):
    return db.query(Exercise).filter(
        Exercise.user_id == current_exercise.id
    ).all()