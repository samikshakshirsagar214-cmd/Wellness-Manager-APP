from pydantic import BaseModel

class WaterCreate(BaseModel):
    amount_ml: int