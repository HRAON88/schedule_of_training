from app.database.models.schedules import ScheduleModel
from app.services.core import Core
from app.telegram_bot.settings import END_ROUTES
from app.telegram_bot.states.base import State
from app.utils.keyboard import KeyBoardFactory


class JoinToTraining(State):
    state = "JoinToTraining"

    async def run(self):
        base = Core()
        await self.query.answer()
        keyboard = KeyBoardFactory()
        context = self.get_context()
        schedule = ScheduleModel(**context["schedule"])
        base.join_to_train(self.user.id, schedule.id)
        await self.query.edit_message_text(
            text="Вы успешно присоединились к тренировке",
            reply_markup=keyboard.generate()
        )
        return END_ROUTES
