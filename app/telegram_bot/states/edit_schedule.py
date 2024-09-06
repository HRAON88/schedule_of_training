from app.services.user_flow_admin import UserFlowAdmin
from app.telegram_bot.settings import END_ROUTES
from app.telegram_bot.states.base import State
from app.utils.keyboard import KeyBoardFactory


class EditSchedule(State):
    state = "EditSchedule"

    async def run(self):
        await self.query.answer()
        flow = UserFlowAdmin()
        keyboard = KeyBoardFactory()
        context = self.get_context()
        time_start, time_end = context["time"].split(" - ")
        flow.edit_schedule(context["schedule"]["id"], context["schedule"]["date"], time_start, time_end)
        await self.query.edit_message_text(text="Расписание успешно изменено", reply_markup=keyboard.generate())
        return END_ROUTES
