from app.services.core import Core
from app.telegram_bot.states.base import State
from app.telegram_bot.states.show_actions_with_schedules import ShowActionsWithMySchedules
from app.utils.keyboard import KeyBoardFactory


class ShowMySchedules(State):
    state = "ShowMySchedules"

    async def run(self):
        await self.query.answer()
        base = Core()
        keyboard = KeyBoardFactory(2)
        user_schedules = {logs.schedule_id for logs in base.get_schedules_by_user(self.user.id)}
        for schedule in base.show_schedules():
            if schedule.id not in user_schedules:
                continue
            text = f"{schedule.sport}: {schedule.t_start} - {schedule.t_end} {schedule.date} Участников:{schedule.participants}"
            trace_id = self.create_trace_id()
            keyboard.go_to_new_line()
            keyboard.add_item(text, ShowActionsWithMySchedules.state, trace_id)
            keyboard.go_to_new_line()
            self.set_context(trace_id, {"schedule": schedule.to_dict(), "user": base.get_user(self.user.id).to_dict()})
        await self.query.edit_message_text(
            text="Выберете тренировку для взаимодействия с ней",
            reply_markup=keyboard.generate(),
        )
        return self.state
