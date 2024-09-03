from app.database.models.base import BaseModel


class SchemeParticipated(BaseModel):
    firstname: str
    lastname: str
    schedule_id: int
