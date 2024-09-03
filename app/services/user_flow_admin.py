import datetime

from app.database.connection import Connection
from app.database.models.schedules import ScheduleModel
from app.database.models.user import UserModel
from app.database.repository.schedules import SchedulesRepository
from app.database.repository.users import UsersRepository


class UserFlowAdmin:

    def create_schedule(self, date: str, t_start: str, t_end: str, sport_id: int):
        with Connection() as c:
            repository = SchedulesRepository(c)
            model = ScheduleModel(
                date=date,
                t_start=t_start,
                t_end=t_end,
                sport_id=sport_id,
            )
            repository.add(model)

    def delete_schedule(self, id_outer):
        with Connection() as c:
            repository = SchedulesRepository(c)
            model = repository.get_by_id(id_outer)
            if model:
                repository.delete(model)

    def show_schedules(self):
        with Connection() as c:
            repository = SchedulesRepository(c)
            return repository.get_all()

    def edit_schedule(self, id_outer, date, t_start, t_end):
        with Connection() as c:
            repository = SchedulesRepository(c)
            model: ScheduleModel = repository.get_by_id(id_outer)
            if model:
                model.date = date
                model.t_start = t_start
                model.t_end = t_end
                repository.update(model, id_outer)

    def change_user(self, firstname_user, lastname_user, role_id_user, id_outer):
        with Connection as c:
            repository = UsersRepository(c)
            model: UserModel = repository.get_by_id(id_outer)
            if model:
                model.firstname = firstname_user
                model.lastname = lastname_user
                model.role_id = role_id_user
                repository.update(model, id_outer)
