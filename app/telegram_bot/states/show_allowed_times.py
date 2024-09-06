from app.database.connection import Connection
from app.database.models.schedules import ScheduleModel
from app.database.repository.schedules import SchedulesRepository
from app.telegram_bot.states.base import State
from app.telegram_bot.states.create_schedule import CreateSchedule
from app.telegram_bot.states.edit_schedule import EditSchedule
from app.utils.keyboard import KeyBoardFactory


class ShowAllowedTimesForEdit(State):
    state = "ShowAllowedTimesForEdit"

    async def run(self):
        await self.query.answer()
        keyboard = KeyBoardFactory()
        context = self.get_context()
        with Connection() as con:
            repository = SchedulesRepository(con)
            date = self.get_selected_date(context)
            sport_id = self.get_selected_sport(context)
            schedules: list[ScheduleModel] = repository.get_all_by_date_and_sport(date, sport_id)
        exist_schedules = {(schedule.t_start, schedule.t_end) for schedule in schedules}
        available_times = [
            f"{hour}:00 - {hour + 1}:00" for hour in range(8, 21) if
            (f"{hour}:00", f"{hour + 1}:00") not in exist_schedules
        ]
        for item in available_times:
            trace_id = self.create_trace_id()
            self.set_context(trace_id, {"time": item})
            keyboard.add_item(item, self.next_state(), trace_id)
        await self.query.edit_message_text(text=self.get_message_text(), reply_markup=keyboard.generate())
        return self.state

    @staticmethod
    def get_message_text():
        return "На какое время перенести занятие?"

    @staticmethod
    def next_state():
        return EditSchedule.state

    @staticmethod
    def get_selected_date(context):
        return context["schedule"]["date"]

    @staticmethod
    def get_selected_sport(context):
        return context["schedule"]["sport_id"]


class ShowAllowedTimesForCreate(ShowAllowedTimesForEdit):
    state = "ShowAllowedTimesForCreate"

    @staticmethod
    def get_message_text():
        return "На какое время создать занятие?"

    @staticmethod
    def next_state():
        return CreateSchedule.state

    @staticmethod
    def get_selected_date(context):
        return context["day"]

    @staticmethod
    def get_selected_sport(context):
        return context["sport"]["id"]
