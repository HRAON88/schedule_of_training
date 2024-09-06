import datetime
from calendar import monthrange

from app.telegram_bot.states.base import State
from app.telegram_bot.states.choose_sport import ChooseSport
from app.utils.keyboard import KeyBoardFactory


class ChooseDate(State):
    state = "ChooseDate"

    async def run(self):
        await self.query.answer()
        today = datetime.date.today()
        days = [
            datetime.date(year=today.year, month=today.month, day=day).strftime("%d.%m.%Y")
            for day in range(today.day, monthrange(today.year, today.month)[1] + 1)
        ]
        keyboard = KeyBoardFactory()
        for day in days:
            trace_id = self.create_trace_id()
            self.set_context(trace_id, {"day": day})
            keyboard.add_item(day, ChooseSport.state, trace_id)
        await self.query.edit_message_text(text="Выберете дату", reply_markup=keyboard.generate())
        return self.state
