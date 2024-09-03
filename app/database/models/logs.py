from app.database.models.base import BaseModel


class LogsModel(BaseModel):
    userid: int
    schedule_id: int
