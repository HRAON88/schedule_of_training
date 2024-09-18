from app.database.models.logs import LogsModel
from app.database.models.schedules import ScheduleModel
from app.database.repository.base import BaseFunction
from app.database.repository.logs import LogsRepository
from app.database.repository.schedules import SchedulesRepository
from app.database.connection import Connection
from app.database.repository.users import UsersRepository
from app.schemes.participated import SchemeParticipated


class UserFlowCoach:
    def join_to_train(self, item_id, user_id, scheduleid):
        with Connection() as c:
            repository = LogsRepository(c)
            model = LogsModel(
                id=item_id,
                userid=user_id,
                scheduleid=scheduleid
            )
            repository.add(model)

    def refuse_to_train(self, user_id, schedule_id):
        with Connection() as c:
            repository = LogsRepository(c)
            model = repository.find_log(user_id, schedule_id)
            repository.delete(model)

    def show_my_schedule(self, user_id):
        with Connection() as c:
            repository = SchedulesRepository(c)
            schedules = repository.find_schedules_by_coach(user_id)
            result = repository.find_who_will_go(*[i.id for i in schedules])
            dictionary = {}
            for model in result:
                if model.scheduleid not in dictionary:
                    dictionary[model.scheduleid] = []
                dictionary[model.scheduleid].append(f'{model.lastname} {model.firstname}')

            for model in schedules:
                model.participated = dictionary.get(model.id, [])
            return schedules

    def show_users(self, schedule_id):
        with Connection() as c:
            repository1 = LogsRepository(c)
            repository2 = UsersRepository(c)
            result = repository1.count_of_users(schedule_id)
            spisok = []
            if result:
                for count, user in enumerate(result, start=1):
                    all_information = repository2.get_by_id(user[0])
                    full_name_user = f'{count}) '

                    if all_information.firstname !='null':
                        full_name_user += all_information.firstname
                        full_name_user += ' '
                    if all_information.lastname != 'null':
                        full_name_user += all_information.lastname
                        full_name_user += ' '
                    if all_information.username !='null':
                        full_name_user += f'@{all_information.username}'
                    spisok.append(full_name_user)
            return spisok



