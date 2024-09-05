from app.database.connection import Connection
from app.database.repository.logs import LogsRepository


class UserFlowCoach:
    def refuse_to_train(self, user_id, schedule_id):
        with Connection() as c:
            repository = LogsRepository(c)
            model = repository.find_log(user_id, schedule_id)
            repository.delete(model)
