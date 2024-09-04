import dataclasses
from app.database.models.base import BaseModel


@dataclasses.dataclass
class ScheduleModel(BaseModel):
    #id: int
    id: int
    dtstart: str
    dtend: str
    sportid: int
