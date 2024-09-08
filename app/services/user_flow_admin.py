from app.database.connection import Connection
from app.database.models.schedules import ScheduleModel
from app.database.models.user import UserModel
from app.database.repository.logs import LogsRepository
from app.database.repository.schedules import SchedulesRepository
from app.database.repository.users import UsersRepository


class UserFlowAdmin:
    def show_all_schedules(self):
        with Connection() as c:
            repository = SchedulesRepository(c)
            return repository.get_all()


    def create_schedule(self, dtstart_user, dtend_user, sportid_user):
        with Connection() as c:
            repository = SchedulesRepository(c)
            model = ScheduleModel(
                t_start=dtstart_user,
                t_end=dtend_user,
                sport_id=sportid_user
            )
            repository.add(model)

    def delete_schedule(self, id_outer):
        with Connection() as c:
            repository = SchedulesRepository(c)
            model = repository.get_by_id(id_outer)
            if model:
                repository.delete(model)

    def edit_schedule(self, id_outer=None, t_start_user=None, t_end_user=None, sport_id_user=None):
        with Connection() as c:
            repository = SchedulesRepository(c)
            model: ScheduleModel = repository.get_by_id(id_outer)
            if model:
                model.t_start = t_start_user
                model.t_end = t_end_user
                model.sport_id = sport_id_user
                repository.update(model, id_outer)

    def change_user_role(self, user_id, role_id):
        with Connection()as c:
            repository = UsersRepository(c)
            model: UserModel = repository.get_by_id(user_id)
            if model:
                model.role_id = role_id
                repository.update(model, user_id)

    def show_all_users_by_admin(self):
        with Connection() as c:
            repository = UsersRepository(c)
            return repository.get_all()