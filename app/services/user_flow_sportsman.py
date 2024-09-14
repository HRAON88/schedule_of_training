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
                return
            model = LogsModel(users_id=user_id, schedule_id=schedule_id)
            return repository.add(model)

    def refuse_to_train(self, user_id, schedule_id):
        with Connection() as c:
            repository = LogsRepository(c)
            model = repository.find_log(user_id, schedule_id)
            if model:
                repository.delete(model)

    def show_schedule(self, user_id):
        with Connection() as c:
            repository = LogsRepository(c)
            result = repository.find_logs(user_id)
            return result

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
            repository = LogsRepository(c)
            result = repository.find_logs(user_id)
            print(result)
            schedules = []

            for value in result:
                cc = UserFlowAdmin().transformation(repository.find_logs(value.schedule_id))
                schedules.append(cc)
                print(cc)
            return schedules
