from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from app.telegram_bot.settings import END_ROUTES


async def show_allowed_schedules(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Вернуться в меню", callback_data="back_to_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f"show_allowed_schedules", reply_markup=reply_markup)
    return END_ROUTES