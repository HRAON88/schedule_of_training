import dataclasses

from app.database.models.base import BaseModel


class UserModel(BaseModel):
    firstname: str
    lastname: str
    username: str
    role_id: int

    def is_admin(self):
        return self.role_id == 1

    def is_coach(self):
        return self.role_id == 2

    def is_sportsman(self):
        return self.role_id == 3
