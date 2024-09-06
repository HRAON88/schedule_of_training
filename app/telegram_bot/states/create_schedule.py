from app.services.user_flow_admin import UserFlowAdmin
from app.telegram_bot.settings import END_ROUTES
from app.telegram_bot.states.base import State
from app.utils.keyboard import KeyBoardFactory


class CreateSchedule(State):
    state = "CreateSchedule"

    async def run(self):
        await self.query.answer()
        context = self.get_context()
        time_start, time_end = context["time"].split(" - ")
        keyboard = KeyBoardFactory()
        flow = UserFlowAdmin()
        flow.create_schedule(context["day"], time_start, time_end, context["sport"]["id"])
        await self.query.edit_message_text(
            text=f"Создана тренировка {context['day']} с {time_start} до {time_end}. Вид спорта: {context['sport']['sport']}",
            reply_markup=keyboard.generate(),
        )
        return END_ROUTES
