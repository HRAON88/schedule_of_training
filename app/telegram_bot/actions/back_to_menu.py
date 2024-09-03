from telegram import Update
from telegram.ext import ContextTypes

from app.telegram_bot.settings import START_ROUTES


async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(text=f"back_to_menu")
    return START_ROUTES
