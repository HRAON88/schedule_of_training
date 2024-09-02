from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from app.services.core import Core
from app.telegram_bot.settings import START_ROUTES


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
    if user.is_admin():
        keyboard = [
            [
                InlineKeyboardButton("Создать расписание", callback_data="create_schedule"),
                InlineKeyboardButton("Удалить расписание", callback_data="delete_schedule"),
                InlineKeyboardButton("Изменить расписание", callback_data="edit_schedule"),
            ],
            [InlineKeyboardButton("Изменить пользователя", callback_data="edit_user_role")],
        ]
    elif user.is_sportsman():
        keyboard = [
            [
                InlineKeyboardButton("Показать мое расписание", callback_data="show_my_schedules"),
                InlineKeyboardButton("Показать доступные тренировки", callback_data="show_allowed_schedules"),
            ],
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    await query.edit_message_text(text="Выберете действие", reply_markup=reply_markup)
    return START_ROUTES