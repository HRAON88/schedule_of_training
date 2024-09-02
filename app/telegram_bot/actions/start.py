from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from app.services.core import Core
from app.telegram_bot.settings import START_ROUTES


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message with three inline buttons attached."""
    core = Core()
    tg_user = update.message.from_user
    user = core.get_user(tg_user.id)
    if not user and core.is_admin_mode():
        user = core.add_admin_user(tg_user.id, tg_user.first_name, tg_user.last_name, tg_user.username)
    elif not user:
        user = core.add_basic_user(tg_user.id, tg_user.first_name, tg_user.last_name, tg_user.username)

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
    elif user.is_coach():
        keyboard = [
            [InlineKeyboardButton("Вернуться в меню", callback_data="back_to_menu")],
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("Вернуться в меню", callback_data="back_to_menu")],
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Выберете действие", reply_markup=reply_markup)
    return START_ROUTES
