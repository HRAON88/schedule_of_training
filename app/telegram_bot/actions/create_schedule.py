from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from app.services.user_flow_admin import UserFlowAdmin
from app.telegram_bot.settings import START_ROUTES, END_ROUTES


async def create_schedule_step_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    available_times = [f"{hour}:00 - {hour + 1}:00" for hour in range(8, 21)]
    col_count = 4
    keyboard = []
    index = 0
    for _ in range((len(available_times) // col_count) + 1):
        row = []
        for _ in range(col_count):
            if index >= len(available_times):
                break
            row.append(InlineKeyboardButton(available_times[index], callback_data=f"create_schedule_time_{available_times[index]}"))
            index += 1
        keyboard.append(row)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Выберете время", reply_markup=reply_markup
    )
    return START_ROUTES


async def create_schedule_step_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    time_start, time_end = query.data.lstrip("create_schedule_time_").split(" - ")
    keyboard = [
        [InlineKeyboardButton("Вернуться в меню", callback_data="back_to_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f"Вы выбрали: {time_start, time_end}", reply_markup=reply_markup)
    return END_ROUTES