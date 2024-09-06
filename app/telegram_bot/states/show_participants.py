from app.services.core import Core
from app.telegram_bot.settings import END_ROUTES
from app.telegram_bot.states.base import State
from app.utils.keyboard import KeyBoardFactory


class ShowParticipants(State):
    state = "ShowParticipants"

    async def run(self):
        await self.query.answer()
        keyboard = KeyBoardFactory()
        base = Core()
        context = self.get_context()
        participants = base.get_participants(context["schedule"]["id"])
        for item in participants:
            keyboard.add_item(item.to_str())
        await self.query.edit_message_text(text="Участники", reply_markup=keyboard.generate())
        return END_ROUTES
