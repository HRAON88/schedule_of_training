from app.services.user_flow_admin import UserFlowAdmin
from app.telegram_bot.states.base import State
from app.telegram_bot.states.choose_user_role import ChooseUserRole
from app.utils.keyboard import KeyBoardFactory


class ShowAllUsers(State):
    state = "ShowAllUsers"

    async def run(self):
        await self.query.answer()
        flow = UserFlowAdmin()
        keyboard = KeyBoardFactory(2)
        for user in flow.get_users():
            trace_id = self.create_trace_id()
            keyboard.add_item(user.to_str(), ChooseUserRole.state, trace_id)
            self.set_context(trace_id, {"user": user.to_dict()})
        await self.query.edit_message_text(text=f"Выберете пользователя", reply_markup=keyboard.generate())
        return self.state
