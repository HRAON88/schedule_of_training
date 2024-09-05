from app.database.models.base import BaseModel


class UserModel(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    username: str | None = None
    role_id: int

    def is_admin(self):
        return self.role_id == 1

    def is_coach(self):
        return self.role_id == 2

    def is_sportsman(self):
        return self.role_id == 3

    def to_str(self):
        text = ""
        if self.is_admin():
            text = "Admin"
        elif self.is_coach():
            text = "Coach"
        elif self.is_sportsman():
            text = "Sportsman"

        if self.lastname and self.lastname.strip() not in ("null", ""):
            text += f" {self.lastname}"
        if self.firstname and self.firstname.strip() not in ("null", ""):
            text += f" {self.firstname}"
        if self.username and self.username.strip() not in ("null", ""):
            text += f" ({self.username})"
        return text
