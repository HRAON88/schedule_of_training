import dataclasses

from app.database.models.base import BaseModel


class SchemeParticipated(BaseModel):
    firstname: str
    lastname: str
    scheduleid: int