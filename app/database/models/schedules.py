from app.database.models.base import BaseModel


class ScheduleModel(BaseModel):
    date: str
    t_start: str
    t_end: str
    sport_id: int
