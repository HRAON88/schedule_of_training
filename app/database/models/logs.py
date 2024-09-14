import dataclasses
from app.database.models.base import BaseModel


class LogsModel(BaseModel):

    users_id: int
    schedule_id: int
    id: int | None = None