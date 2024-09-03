from app.database.models.schedules import ScheduleModel
from app.database.repository.base import BaseFunction
from app.schemes.detailedschedule import ScheduleModelDetail
from app.schemes.participated import SchemeParticipated


class SchedulesRepository(BaseFunction):
    table = "schedules"
    model = ScheduleModel

    def find_schedules_by_user(self, user_id):
        self.cur.execute(
            f"""
            SELECT 
            {self.table}.*,
            sports.sport
            FROM {self.table}
            INNER JOIN logs on sports.id = {self.table}.sports_id
            WHERE userid = {user_id}
        """
        )
        names = [description[0] for description in self.cur.description]
        return [ScheduleModelDetail(**{col: val for val, col in zip(item, names)}) for item in self.cur.fetchall()]

    def get_all(self):
        self.cur.execute(
            f"""
                SELECT 
                {self.table}.*,
                sports.sport as sport
                FROM {self.table}
                INNER JOIN sports on sports.id = {self.table}.sport_id
            """
        )
        names = [description[0] for description in self.cur.description]
        return [ScheduleModelDetail(**{col: val for val, col in zip(item, names)}) for item in self.cur.fetchall()]
    def find_who_will_go(self, *schedule_id):
        self.cur.execute(
            f"""
            SELECT users.firstname, users.lastname, logs.schedule_id
            FROM logs
            INNER JOIN users on logs.userid
            WHERE schedule_id in {schedule_id} AND users.role_id != 2"""
        )
        names = [description[0] for description in self.cur.description]
        return [SchemeParticipated(**{col: val for val, col in zip(item, names)}) for item in self.cur.fetchall()]

    def get_all_by_date_and_sport(self, date: str, sport_id: int):
        self.cur.execute(
            f"""
            SELECT *
            FROM {self.table}
            WHERE date = '{date}' and sport_id = {sport_id}
            """
        )
        names = [description[0] for description in self.cur.description]
        return [self.model(**{col: val for val, col in zip(item, names)}) for item in self.cur.fetchall()]
