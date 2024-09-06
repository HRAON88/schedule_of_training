import uuid

from app.services.core import Core
from app.telegram_bot.states.base import State
from app.telegram_bot.states.show_actions_with_schedules import ShowActionsWithSchedules
from app.utils.keyboard import KeyBoardFactory


class ShowSchedules(State):
    state = "ShowSchedules"

    async def run(self):
        await self.query.answer()
        base = Core()
        keyboard = KeyBoardFactory(2)
        context = self.get_context()
        user_schedules = {logs.schedule_id for logs in base.get_schedules_by_user(self.user.id)}
        for schedule in base.show_schedules():
            if schedule.id in user_schedules:
                continue
            text = f"{schedule.sport}: {schedule.t_start} - {schedule.t_end} {schedule.date}"
            trace_id = self.create_trace_id()
            if schedule.participants:
                text += f" Участников:{schedule.participants}"
                keyboard.go_to_new_line()
                keyboard.add_item(text, ShowActionsWithSchedules.state, trace_id)
                keyboard.go_to_new_line()
            else:
                keyboard.add_item(text, ShowActionsWithSchedules.state, trace_id)
            context[trace_id] = {"schedule": schedule.to_dict()}
        await self.query.edit_message_text(text="Выберете занятие", reply_markup=keyboard.generate())
        return self.state
