from app.database.models.roles import RolesModel
from app.database.repository.base import BaseFunction


class RolesRepository(BaseFunction):
    table = "roles"
    model = RolesModel

    def get_by_role(self, role):
        query = f"select * from {self.table} where role='{role}'"
        self.cur.execute(query)
        result = self.cur.fetchone()
        if result:
            return self.model(*result)
