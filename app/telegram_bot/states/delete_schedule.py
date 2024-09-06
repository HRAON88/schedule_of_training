from app.services.user_flow_admin import UserFlowAdmin
from app.telegram_bot.settings import END_ROUTES
from app.telegram_bot.states.base import State
from app.utils.keyboard import KeyBoardFactory


class DeleteSchedule(State):
    state = "DeleteSchedule"

    async def run(self):
        await self.query.answer()
        flow = UserFlowAdmin()
        keyboard = KeyBoardFactory()
        context = self.get_context()
        flow.delete_schedule(context["schedule"]["id"])
        await self.query.edit_message_text(text="Расписание успешно удалено", reply_markup=keyboard.generate())
        return END_ROUTES
