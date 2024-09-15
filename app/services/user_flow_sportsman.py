from app.database.connection import Connection
from app.database.models.logs import LogsModel
from app.database.models.schedules import ScheduleModel
from app.database.repository.logs import LogsRepository
from app.database.repository.schedules import SchedulesRepository
from app.services.user_flow_admin import UserFlowAdmin


class UserFlowSportsman:
    def join_to_train(self, user_id, schedule_id):
        with Connection() as c:
            repository = LogsRepository(c)
            is_exist = repository.find_log(user_id, schedule_id)
            if is_exist:
                return False
            model = LogsModel(users_id=user_id, schedule_id=schedule_id)
            return repository.add(model)

    def refuse_to_train(self, id):
        with Connection() as c:
            repository = LogsRepository(c)
            model = repository.find_log_by_id(id)
            if model:
                repository.delete(model)
                return True
            else:
                return False
    def show_schedule(self, user_id):
        with Connection() as c:
            repository = LogsRepository(c)
            result = repository.find_logs(user_id)
            return UserFlowAdmin().transformation()

    def show_all_schedules(self, user_id):
        with Connection() as c:
            repository = SchedulesRepository(c)
            result = repository.get_all_sportsman()
            return result

    # def show_schedules(self) -> list[ScheduleModel]:
    #     with Connection() as c:
    #         repository = SchedulesRepository(c)
    #         schedules = sorted(
    #             repository.get_all(),
    #             key=lambda x: (x == True)),
    #
    #         return schedules




    def show_all_booked_schedules(self, user_id):
        with Connection() as c:
            repository1 = LogsRepository(c)
            repository2 = SchedulesRepository(c)
            result = repository1.find_logs(user_id)
            schedules = []
            if result:
                for count, value in enumerate(result, start=1):
                    end = UserFlowAdmin().transformation2(repository2.get_all_sportsman_schedules(value.schedule_id))
                    result = f'{count}) {end}+{value.id}'
                    schedules.append(result)
                return schedules
            else:
                return False
