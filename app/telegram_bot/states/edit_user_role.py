from app.services.user_flow_admin import UserFlowAdmin
from app.telegram_bot.settings import END_ROUTES
from app.telegram_bot.states.base import State
from app.utils.keyboard import KeyBoardFactory


class EditUserRole(State):
    state = "EditUserRole"

    async def run(self):
        await self.query.answer()
        flow = UserFlowAdmin()
        keyboard = KeyBoardFactory()
        context = self.get_context()
        flow.change_user_role(context["user"]["id"], context["role"]["id"])
        await self.query.edit_message_text(
            text=f"Пользователь получил роль '{context['role']['role']}'", reply_markup=keyboard.generate()
        )
        return END_ROUTES
