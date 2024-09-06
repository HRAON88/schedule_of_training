from app.services.core import Core
from app.telegram_bot.states.base import State
from app.telegram_bot.states.show_allowed_times import ShowAllowedTimesForCreate
from app.utils.keyboard import KeyBoardFactory


class ChooseSport(State):
    state = "ChooseSport"

    async def run(self):
        await self.query.answer()
        base = Core()
        sports = base.get_sports()
        keyboard = KeyBoardFactory()
        for sport in sports:
            trace_id = self.create_trace_id()
            self.set_context(trace_id, {"sport": sport.to_dict()})
            keyboard.add_item(sport.sport, ShowAllowedTimesForCreate.state, trace_id)
        await self.query.edit_message_text(text="Выберете вид спорта", reply_markup=keyboard.generate())
        return ChooseSport.state
