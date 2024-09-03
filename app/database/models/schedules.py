import dataclasses

from app.database.models.base import BaseModel


@dataclasses.dataclass
class ScheduleModel(BaseModel):
    dtstart: str
    dtend: str
    sportid: int
    id: int | None = None
