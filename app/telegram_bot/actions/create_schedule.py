from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from app.database.connection import Connection
from app.database.repository.sports import SportsRepository
from app.services.user_flow_admin import UserFlowAdmin
from app.telegram_bot.settings import START_ROUTES, END_ROUTES


async def create_schedule_step_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    with Connection() as con:
        repository = SportsRepository(con)
        sports = repository.get_all()
    keyboard = [
        [InlineKeyboardButton(sport.sport, callback_data=f"create_schedule_sport_{sport.id}") for sport in sports]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Выберете вид спорта", reply_markup=reply_markup
    )
    return START_ROUTES

async def create_schedule_step_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    sport_id = int(query.data.lstrip("create_schedule_sport_"))
    available_times = [f"{hour}:00 - {hour + 1}:00" for hour in range(8, 21)]
    col_count = 4
    keyboard = []
    index = 0
    for _ in range((len(available_times) // col_count) + 1):
        row = []
        for _ in range(col_count):
            if index >= len(available_times):
                break
            row.append(InlineKeyboardButton(available_times[index], callback_data=f"create_schedule_time_{available_times[index]}_sport_{sport_id}"))
            index += 1
        keyboard.append(row)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Выберете время", reply_markup=reply_markup
    )
    return START_ROUTES


async def create_schedule_step_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()

    time, sport_id = query.data.lstrip("create_schedule_time_").split("_sport_")
    time_start, time_end = time.split(" - ")
    keyboard = [
        [InlineKeyboardButton("Вернуться в меню", callback_data="back_to_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    with Connection() as con:
        repository = SportsRepository(con)
        sport = repository.get_by_id(int(sport_id))

    flow = UserFlowAdmin()
    flow.create_schedule(time_start, time_end, sport.id)
    await query.edit_message_text(text=f"Создана тренировка с {time_start} до {time_end}. Вид спорта: {sport.sport}",
                                  reply_markup=reply_markup)
    return END_ROUTES