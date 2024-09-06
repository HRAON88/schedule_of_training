from app.services.core import Core
from app.telegram_bot.states.base import State
from app.telegram_bot.states.edit_user_role import EditUserRole
from app.utils.keyboard import KeyBoardFactory


class ChooseUserRole(State):
    state = "ChooseUserRole"

    async def run(self):
        await self.query.answer()
        core = Core()
        keyboard = KeyBoardFactory()
        for role in core.get_roles():
            trace_id = self.create_trace_id()
            keyboard.add_item(role.role, EditUserRole.state, trace_id)
            self.set_context(trace_id, {"role": role.to_dict()})
        await self.query.edit_message_text(text=f"Выберете роль", reply_markup=keyboard.generate())
        return self.state
