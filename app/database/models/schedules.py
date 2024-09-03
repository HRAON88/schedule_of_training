import dataclasses

from app.database.models.base import BaseModel


@dataclasses.dataclass
class ScheduleModel(BaseModel):
    date: str
    t_start: str
    t_end: str
    sport_id: int
    id: int | None = None
