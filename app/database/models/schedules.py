import dataclasses
from app.database.models.base import BaseModel



class ScheduleModel(BaseModel):
    #id: int

    t_start: str
    t_end: str
    sport_id: int
    id: int | None = None