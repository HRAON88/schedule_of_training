from app.database.models.schedules import ScheduleModel
from app.database.repository.base import BaseFunction
from app.schemes.detailedschedule import ScheduleModelDetail
from app.schemes.participated import SchemeParticipated


class SchedulesRepository(BaseFunction):
    table = 'schedules'
    model = ScheduleModel

    def find_schedules_by_coach(self, user_id):
        self.cur.execute(f"""
            SELECT 
            {self.table}.*,
            sports.sport
            FROM {self.table}
            INNER JOIN logs on logs.scheduleid = {self.table}.id
            INNER JOIN logs on sports.id = {self.table}.sport_id
            WHERE userid = {user_id}
        """)
        return [ScheduleModelDetail(*i) for i in self.cur.fetchall()]

    def find_who_will_go(self, *schedule_id):
        self.cur.execute(f'''
            SELECT users.firstname, users.lastname, logs.schedule_id
            FROM logs
            INNER JOIN users on logs.users_id
            WHERE schedule_id in {schedule_id} AND users.roleid != 2''')
        return [SchemeParticipated(*i) for i in self.cur.fetchall()]

    def find_schedule(self, schedule_id):
        self.cur.execute(f"SELECT * FROM {self.table} WHERE id = {schedule_id}")
        result = self.cur.fetchone()
        if result:
            names = [description[0] for description in self.cur.description]
            return [self.model(**{col: val for val, col in zip(item, names)}) for item in result]
        return []


    def get_all_sportsman_schedules(self, id):
        self.cur.execute(f'select * from {self.table} WHERE id = {id}')
        p = self.cur.fetchone()
        return p

