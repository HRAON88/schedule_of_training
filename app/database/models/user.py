import dataclasses

from app.database.models.base import BaseModel


@dataclasses.dataclass
class UserModel(BaseModel):
    id: int | None = None
    firstname: str | None = None
    lastname: str | None = None
    roleid: int | None = None

    def is_admin(self):
        return self.roleid == 1

    def is_coach(self):
        return self.roleid == 2

    def is_sportsman(self):
        return self.roleid == 3
