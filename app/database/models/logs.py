import dataclasses
from app.database.models.base import BaseModel


class LogsModel(BaseModel):

    userid: int
    scheduleid: int
    id: int | None = None