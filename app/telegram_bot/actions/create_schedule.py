import datetime
import json
import uuid
from calendar import monthrange

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.database.connection import Connection
from app.database.models.schedules import ScheduleModel
from app.database.repository.schedules import SchedulesRepository
from app.database.repository.sports import SportsRepository
from app.schemes.callback_data import CallBackData
from app.services.user_flow_admin import UserFlowAdmin
from app.telegram_bot.settings import END_ROUTES, START_ROUTES
from app.user_flow_storage import user_flow_storage


async def create_schedule_step_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    with Connection() as con:
        repository = SportsRepository(con)
        sports = repository.get_all()
    keyboard = [[]]
    user = update.callback_query.from_user
    user_flow_storage[user.id] = {}
    for sport in sports:
        trace_id = uuid.uuid4().hex
        data = {"sport": sport.to_dict()}
        button = InlineKeyboardButton(
            sport.sport, callback_data=CallBackData(tag="cs_1", trace_id=trace_id).model_dump_json()
        )
        keyboard[0].append(button)
        user_flow_storage[user.id][trace_id] = data

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Выберете вид спорта", reply_markup=reply_markup)
    return START_ROUTES


async def create_schedule_step_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user = update.callback_query.from_user
    cache_data = user_flow_storage[user.id][json.loads(update.callback_query.data)["trace_id"]]
    today = datetime.date.today()
    days = [
        datetime.date(year=today.year, month=today.month, day=day).strftime("%d.%m.%Y")
        for day in range(today.day, monthrange(today.year, today.month)[1] + 1)
    ]
    keyboard = []
    col_count = 4
    index = 0
    for _ in range((len(days) // col_count) + 1):
        row = []
        for _ in range(col_count):
            if index >= len(days):
                break
            trace_id = uuid.uuid4().hex
            if trace_id not in user_flow_storage[user.id]:
                user_flow_storage[user.id][trace_id] = {}
            user_flow_storage[user.id][trace_id].update(cache_data)
            user_flow_storage[user.id][trace_id]["day"] = days[index]
            row.append(
                InlineKeyboardButton(
                    days[index], callback_data=CallBackData(tag="cs_2", trace_id=trace_id).model_dump_json()
                )
            )
            index += 1
        keyboard.append(row)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Выберете дату", reply_markup=reply_markup)
    return START_ROUTES


async def create_schedule_step_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user = update.callback_query.from_user
    cache_data = user_flow_storage[user.id][json.loads(update.callback_query.data)["trace_id"]]

    with Connection() as con:
        repository = SchedulesRepository(con)
        schedules: list[ScheduleModel] = repository.get_all_by_date_and_sport(cache_data["day"], cache_data["sport"]["id"])
    exist_schedules = {(schedule.t_start, schedule.t_end)for schedule in schedules}
    available_times = [f"{hour}:00 - {hour + 1}:00" for hour in range(8, 21) if (f"{hour}:00", f"{hour + 1}:00") not in exist_schedules]
    col_count = 4
    keyboard = []
    index = 0
    for _ in range((len(available_times) // col_count) + 1):
        row = []
        for _ in range(col_count):
            if index >= len(available_times):
                break
            trace_id = uuid.uuid4().hex
            if trace_id not in user_flow_storage[user.id]:
                user_flow_storage[user.id][trace_id] = {}
            user_flow_storage[user.id][trace_id].update(cache_data)
            user_flow_storage[user.id][trace_id]["time"] = available_times[index]
            row.append(
                InlineKeyboardButton(
                    available_times[index], callback_data=CallBackData(tag="cs_3", trace_id=trace_id).model_dump_json()
                )
            )
            index += 1
        keyboard.append(row)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Выберете время", reply_markup=reply_markup)
    return START_ROUTES


async def create_schedule_step_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user = update.callback_query.from_user
    cache_data = user_flow_storage[user.id][json.loads(update.callback_query.data)["trace_id"]]
    time_start, time_end = cache_data["time"].split(" - ")
    keyboard = [
        [InlineKeyboardButton("Вернуться в меню", callback_data=CallBackData(tag="back_to_menu").model_dump_json())],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    flow = UserFlowAdmin()
    flow.create_schedule(cache_data["day"], time_start, time_end, cache_data["sport"]["id"])
    await query.edit_message_text(
        text=f"Создана тренировка {cache_data['day']} с {time_start} до {time_end}. Вид спорта: {cache_data['sport']['sport']}",
        reply_markup=reply_markup,
    )
    user_flow_storage.pop(user.id)
    return END_ROUTES
