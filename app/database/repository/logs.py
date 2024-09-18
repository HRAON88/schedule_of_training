from app.database.models.logs import LogsModel
from app.database.repository.base import BaseFunction


class LogsRepository(BaseFunction):
    table = 'logs'
    model = LogsModel

    def find_log(self, user_id, schedule_id):
        self.cur.execute(f"SELECT * FROM {self.table} WHERE users_id = {user_id} and schedule_id = {schedule_id}")
        result = self.cur.fetchone()
        if result:
            names = [description[0] for description in self.cur.description]
            return self.model(**{col: val for val, col in zip(result, names)})

    def find_log_by_id(self, id):
        self.cur.execute(f"SELECT * FROM {self.table} WHERE id = {id}")
        result = self.cur.fetchone()
        if result:
            names = [description[0] for description in self.cur.description]
            return self.model(**{col: val for val, col in zip(result, names)})

    def find_logs(self, user_id):
        self.cur.execute(f"SELECT * FROM {self.table} WHERE users_id = {user_id}")
        result = self.cur.fetchall()
        if result:
            names = [description[0] for description in self.cur.description]
            return [self.model(**{col: val for val, col in zip(item, names)}) for item in result]

    def count_of_users(self, schedule_id):
        self.cur.execute(f"SELECT users_id FROM {self.table} WHERE schedule_id = {schedule_id}")
        result = self.cur.fetchall()
        if result:
            return result
        else: return False


