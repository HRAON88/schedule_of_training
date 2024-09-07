from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.schemes.callback_data import CallBackData
from app.services.core import Core
from app.telegram_bot.settings import START_ROUTES
from app.telegram_bot.states.base import State
from app.telegram_bot.states.choose_date import ChooseDate
from app.telegram_bot.states.show_all_users import ShowAllUsers
from app.telegram_bot.states.show_my_schedules import ShowMySchedules
from app.telegram_bot.states.show_schedules import ShowSchedules
from app.user_flow_storage import user_flow_storage


class Start(State):
    state = "Start"

    async def run(self):
        core = Core()

        user = core.get_user(self.user.id)
        if not user and core.is_admin_mode():
            user = core.add_admin_user(self.user.id, self.user.first_name, self.user.last_name, self.user.username)
        elif not user:
            user = core.add_basic_user(self.user.id, self.user.first_name, self.user.last_name, self.user.username)
        if self.query:
            await self.query.answer()
        user_flow_storage.pop(self.user.id, None)
        if user.is_admin():
            keyboard = [
                [
                    InlineKeyboardButton(
                        "Создать расписание", callback_data=CallBackData(tag=ChooseDate.state).model_dump_json()
                    ),
                    InlineKeyboardButton(
                        "Изменить пользователя", callback_data=CallBackData(tag=ShowAllUsers.state).model_dump_json()
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "Показать доступное расписание",
                        callback_data=CallBackData(tag=ShowSchedules.state).model_dump_json()
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "Показать мое расписание",
                        callback_data=CallBackData(tag=ShowMySchedules.state).model_dump_json()
                    ),
                ],

            ]
        else:
            keyboard = [
                [
                    InlineKeyboardButton(
                        "Показать доступное расписание",
                        callback_data=CallBackData(tag=ShowSchedules.state).model_dump_json()
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "Показать мое расписание",
                        callback_data=CallBackData(tag=ShowMySchedules.state).model_dump_json()
                    ),
                ],
            ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        if self.query:
            await self.query.edit_message_text(text="Выберете действие", reply_markup=reply_markup)
        else:
            await self.message.reply_text(text="Выберете действие", reply_markup=reply_markup)
        return START_ROUTES
