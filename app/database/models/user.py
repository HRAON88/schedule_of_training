import dataclasses

from app.database.models.base import BaseModel


@dataclasses.dataclass
class UserModel(BaseModel):
    id: int
    firstname: str
    lastname: str
    roleid: int

    def is_admin(self):
        return self.roleid == 1

    def is_coach(self):
        return self.roleid == 2

    def is_sportsman(self):
        return self.roleid == 3
