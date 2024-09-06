from datetime import datetime

from app.database.connection import Connection
from app.database.models.logs import LogsModel
from app.database.models.schedules import ScheduleModel
from app.database.models.user import UserModel
from app.database.repository.logs import LogsRepository
from app.database.repository.roles import RolesRepository
from app.database.repository.schedules import SchedulesRepository
from app.database.repository.sports import SportsRepository
from app.database.repository.users import UsersRepository


class Core:
    def is_admin_mode(self):
        with Connection() as c:
            r = UsersRepository(c)
            return len(r.get_all()) == 0

    def get_user(self, user_id) -> UserModel:
        with Connection() as c:
            r = UsersRepository(c)
            return r.get_by_id(user_id)

    def get_roles(self):
        with Connection() as c:
            r = RolesRepository(c)
            return r.get_all()

    def add_admin_user(self, user_id, first_name, last_name, username) -> UserModel:
        with Connection() as c:
            r = UsersRepository(c)
            role_r = RolesRepository(c)
            admin_role = role_r.get_by_role("admin")
            if not admin_role:
                raise ValueError("Admin role not found")
            m = UserModel(
                id=user_id,
                firstname=first_name,
                lastname=last_name,
                username=username,
                role_id=admin_role.id,
            )
            return r.add(m)

    def add_basic_user(self, user_id, first_name, last_name, username) -> UserModel:
        with Connection() as c:
            r = UsersRepository(c)
            role_r = RolesRepository(c)
            admin_role = role_r.get_by_role("sportsman")
            if not admin_role:
                raise ValueError("Admin role not found")
            m = UserModel(
                id=user_id,
                firstname=first_name,
                lastname=last_name,
                username=username,
                role_id=admin_role.id,
            )
            return r.add(m)

    def show_schedules(self) -> list[ScheduleModel]:
        with Connection() as c:
            repository = SchedulesRepository(c)
            schedules = sorted(
                repository.get_all(),
                key=lambda x: (x.sport, datetime.strptime(f"{x.t_start} {x.date}", "%H:%M %d.%m.%Y")),
            )
            return schedules

    def join_to_train(self, user_id, schedule_id):
        with Connection() as c:
            repository = LogsRepository(c)
            is_exist = repository.find_log(user_id, schedule_id)
            if is_exist:
                return
            model = LogsModel(user_id=user_id, schedule_id=schedule_id)
            return repository.add(model)

    def get_schedules_by_user(self, user_id):
        with Connection() as c:
            repository = LogsRepository(c)
            return repository.find_logs(user_id)

    def refuse_to_train(self, user_id, schedule_id):
        with Connection() as c:
            repository = LogsRepository(c)
            model = repository.find_log(user_id, schedule_id)
            repository.delete(model)

    def get_participants(self, schedule_id):
        with Connection() as c:
            repository = LogsRepository(c)
            return repository.get_participants(schedule_id)

    def get_sports(self):
        with Connection() as con:
            repository = SportsRepository(con)
            return repository.get_all()
