from app.services.core import Core
from app.telegram_bot.settings import END_ROUTES
from app.telegram_bot.states.base import State
from app.utils.keyboard import KeyBoardFactory


class RefuseToTrain(State):
    state = "RefuseToTrain"

    async def run(self):
        await self.query.answer()
        keyboard = KeyBoardFactory()
        base = Core()
        context = self.get_context()
        base.refuse_to_train(self.user.id, context["schedule"]["id"])
        await self.query.edit_message_text(text="Вы успешно отказались от тренировки!", reply_markup=keyboard.generate())
        return END_ROUTES
