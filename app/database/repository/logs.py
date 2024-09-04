from app.database.models.logs import LogsModel
from app.database.repository.base import BaseFunction


class LogsRepository(BaseFunction):
    table = 'logs'
    model = LogsModel

    def find_log(self, user_id, schedule_id):
        self.cur.execute(f"SELECT * FROM {self.table} WHERE userid = {user_id} and scheduleid = {schedule_id}")
        result = self.cur.fetchone()
        if result:
            return self.model(*result)

    def find_logs(self, user_id):
        self.cur.execute(f"SELECT * FROM {self.table} WHERE userid = {user_id}")
        result = self.cur.fetchall()
        if result:
            return [self.model(*i) for i in self.cur.fetchall()]

