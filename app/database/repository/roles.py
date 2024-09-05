from app.database.models.roles import RolesModel
from app.database.repository.base import BaseFunction


class RolesRepository(BaseFunction):
    table = 'roles'
    model = RolesModel

    def get_by_role(self, role):
        query = f"select * from {self.table} where role='{role}'"
        self.cur.execute(query)
        result = self.cur.fetchone()
        if result:
            names = [description[0] for description in self.cur.description]
            return self.model(**{col: val for val, col in zip(result, names)})