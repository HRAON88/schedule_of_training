from app.database.connection import Connection
from app.database.models.schedules import ScheduleModel
from app.database.models.user import UserModel
from app.database.repository.logs import LogsRepository
from app.database.repository.schedules import SchedulesRepository
from app.database.repository.users import UsersRepository


class UserFlowAdmin:
    def show_all_logs(self):
        with Connection() as c:
            repository = LogsRepository(c)
            return repository.find_all_logs()


    def create_schedule(self, dtstart_user, dtend_user, sportid_user):
        with Connection() as c:
            repository = SchedulesRepository(c)
            model = ScheduleModel(
                dtstart=dtstart_user,
                dtend=dtend_user,
                sportid=sportid_user
            )
            repository.add(model)

    def delete_schedule(self, id_outer):
        with Connection() as c:
            repository = SchedulesRepository(c)
            model = repository.get_by_id(id_outer)
            if model:
                repository.delete(model)

    def edit_schedule(self, id_outer, dtstart_user, dtend_user, sportid_user):
        with Connection() as c:
            repository = SchedulesRepository(c)
            model: ScheduleModel = repository.get_by_id(id_outer)
            if model:
                model.dtstart = dtstart_user
                model.dtend = dtend_user
                model.sportid = sportid_user
                repository.update(model, id_outer)

    def change_user(self, firstname_user, lastname_user, role_id_user, id_outer):
        with Connection as c:
            repository = UsersRepository(c)
            model: UserModel = repository.get_by_id(id_outer)
            if model:
                model.firstname = firstname_user
                model.lastname = lastname_user
                model.roleid = role_id_user
                repository.update(model, id_outer)
