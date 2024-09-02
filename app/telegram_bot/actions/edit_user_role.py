from telegram import Update
from telegram.ext import ContextTypes

from app.telegram_bot.settings import START_ROUTES


async def edit_user_role(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(text=f"edit_user_role")
    return START_ROUTES