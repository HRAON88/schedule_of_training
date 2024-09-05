from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.schemes.callback_data import CallBackData
from app.services.core import Core
from app.telegram_bot.settings import START_ROUTES
from app.user_flow_storage import user_flow_storage


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message with three inline buttons attached."""
    core = Core()
    tg_user = update.message.from_user
    user = core.get_user(tg_user.id)
    user_flow_storage.pop(tg_user.id, None)
    if not user and core.is_admin_mode():
        user = core.add_admin_user(tg_user.id, tg_user.first_name, tg_user.last_name, tg_user.username)
    elif not user:
        user = core.add_basic_user(tg_user.id, tg_user.first_name, tg_user.last_name, tg_user.username)

    if user.is_admin():
        keyboard = [
            [
                InlineKeyboardButton(
                    "Создать расписание", callback_data=CallBackData(tag="create_schedule").model_dump_json()
                ),
                InlineKeyboardButton(
                    "Удалить расписание", callback_data=CallBackData(tag="delete_schedule").model_dump_json()
                ),
                InlineKeyboardButton(
                    "Изменить расписание", callback_data=CallBackData(tag="edit_schedule").model_dump_json()
                ),
            ],
            [
                InlineKeyboardButton(
                    "Изменить пользователя", callback_data=CallBackData(tag="edit_user_role").model_dump_json()
                )
            ],
            [
                InlineKeyboardButton(
                    "Показать мое расписание", callback_data=CallBackData(tag="show_my_schedules").model_dump_json()
                ),
                InlineKeyboardButton(
                    "Записаться на тренировку",
                    callback_data=CallBackData(tag="join_to_training").model_dump_json(),
                ),
            ],
        ]
    elif user.is_sportsman():
        keyboard = [
            [
                InlineKeyboardButton(
                    "Показать мое расписание", callback_data=CallBackData(tag="show_my_schedules").model_dump_json()
                ),
                InlineKeyboardButton(
                    "Записаться на тренировку",
                    callback_data=CallBackData(tag="join_to_training").model_dump_json(),
                ),
            ],
        ]
    elif user.is_coach():
        keyboard = [
            [
                InlineKeyboardButton(
                    "Вернуться в меню", callback_data=CallBackData(tag="back_to_menu").model_dump_json()
                )
            ],
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton(
                    "Вернуться в меню", callback_data=CallBackData(tag="back_to_menu").model_dump_json()
                )
            ],
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Выберете действие", reply_markup=reply_markup)
    return START_ROUTES
