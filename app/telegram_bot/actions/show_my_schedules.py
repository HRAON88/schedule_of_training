from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.schemes.callback_data import CallBackData
from app.telegram_bot.settings import END_ROUTES


async def show_my_schedules(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Вернуться в меню", callback_data=CallBackData(tag="back_to_menu").model_dump_json())],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f"show_allowed_schedules", reply_markup=reply_markup)
    return END_ROUTES
