import dataclasses
from app.database.models.base import BaseModel


@dataclasses.dataclass
class LogsModel(BaseModel):

    userid: int
    scheduleid: int
    id: int | None = None