from app.database.connection import Connection
from app.database.repository.logs import LogsRepository


class UserFlowSportsman:

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
