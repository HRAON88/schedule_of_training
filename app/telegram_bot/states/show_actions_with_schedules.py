from app.services.core import Core
from app.telegram_bot.states.base import State
from app.telegram_bot.states.delete_schedule import DeleteSchedule
from app.telegram_bot.states.join_to_training import JoinToTraining
from app.telegram_bot.states.refuse_to_train import RefuseToTrain
from app.telegram_bot.states.show_allowed_times import ShowAllowedTimesForEdit
from app.telegram_bot.states.show_participants import ShowParticipants
from app.utils.keyboard import KeyBoardFactory


class ShowActionsWithSchedules(State):
    state = "ShowActionsWithSchedules"

    async def run(self):
        await self.query.answer()
        keyboard = KeyBoardFactory(2)
        for action, tag in self.get_allowed_actions():
            trace_id = self.create_trace_id()
            keyboard.add_item(action, tag, trace_id)
            self.set_context(trace_id, {})
        await self.query.edit_message_text(text="Выберете действие", reply_markup=keyboard.generate())
        return self.state

    def get_allowed_actions(self) -> list[tuple[str, str]]:
        base = Core()
        actions = []
        db_user = base.get_user(self.user.id)
        user_schedules = {logs.schedule_id for logs in base.get_schedules_by_user(self.user.id)}
        if db_user.is_admin():
            actions.append(("Удалить", DeleteSchedule.state))
            actions.append(("Изменить", ShowAllowedTimesForEdit.state))
        context = self.get_context()
        schedule_id = context["schedule"]["id"]
        if schedule_id not in user_schedules:
            actions.append(("Записаться на тренировку", JoinToTraining.state))
        return actions


class ShowActionsWithMySchedules(ShowActionsWithSchedules):
    state = "ShowActionsWithMySchedules"

    def get_allowed_actions(self) -> list[tuple[str, str]]:
        actions = [
            ("Отказаться от тренировки", RefuseToTrain.state),
            ("Показать участников", ShowParticipants.state),
        ]
        return actions
