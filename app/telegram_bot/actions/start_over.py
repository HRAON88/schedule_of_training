from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.schemes.callback_data import CallBackData
from app.services.core import Core
from app.telegram_bot.settings import START_ROUTES
from app.user_flow_storage import user_flow_storage


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    core = Core()
    tg_user = update.callback_query.from_user
    user = core.get_user(tg_user.id)
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    user_flow_storage.pop(tg_user.id, None)
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
        ]
    elif user.is_sportsman():
        keyboard = [
            [
                InlineKeyboardButton(
                    "Показать мое расписание", callback_data=CallBackData(tag="show_my_schedules").model_dump_json()
                ),
                InlineKeyboardButton(
                    "Показать доступные тренировки",
                    callback_data=CallBackData(tag="show_allowed_schedules").model_dump_json(),
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
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    await query.edit_message_text(text="Выберете действие", reply_markup=reply_markup)
    return START_ROUTES
