from app.database.models.base import BaseModel


class LogsModel(BaseModel):
    user_id: int
    schedule_id: int
