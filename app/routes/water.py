from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.core.deps import get_current_user
from app.models.water import Water
from app.schemas.water import WaterCreate

router = APIRouter(prefix="/water", tags=["Water"])

@router.post("/")
def add_water(data: WaterCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    water = Water(user_id=user.id, amount_ml=data.amount_ml)
    db.add(water)
    db.commit()
    db.refresh(water)
    return water