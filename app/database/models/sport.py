import dataclasses
from app.database.models.base import BaseModel



class SportsModel(BaseModel):
    id: int
    sport: str
