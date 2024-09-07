from app.database.models.logs import LogsModel
from app.database.models.user import UserModel
from app.database.repository.base import BaseFunction


class LogsRepository(BaseFunction):
    table = "logs"
    model = LogsModel

    def find_log(self, user_id, schedule_id):
        self.cur.execute(f"SELECT * FROM {self.table} WHERE user_id = {user_id} and schedule_id = {schedule_id}")
        result = self.cur.fetchone()
        if result:
            names = [description[0] for description in self.cur.description]
            return self.model(**{col: val for val, col in zip(result, names)})

    def get_participants(self, schedule_id):
        self.cur.execute(
            f"""
                SELECT 
                    users.* 
                FROM {self.table} 
                JOIN users on users.id = {self.table}.user_id
                WHERE {self.table}.schedule_id = {schedule_id}
                
            """
        )
        result = self.cur.fetchall()
        if result:
            names = [description[0] for description in self.cur.description]
            return [UserModel(**{col: val for val, col in zip(item, names)}) for item in result]
        return []

    def find_logs(self, user_id):
        self.cur.execute(f"SELECT * FROM {self.table} WHERE user_id = {user_id}")
        result = self.cur.fetchall()
        if result:
            names = [description[0] for description in self.cur.description]
            return [self.model(**{col: val for val, col in zip(item, names)}) for item in result]
        return []