import json
import uuid

from telegram import Update
from telegram.ext import ContextTypes

from app.database.connection import Connection
from app.database.models.schedules import ScheduleModel
from app.database.repository.schedules import SchedulesRepository
from app.services.core import Core
from app.services.user_flow_admin import UserFlowAdmin
from app.telegram_bot.settings import END_ROUTES, START_ROUTES
from app.user_flow_storage import user_flow_storage
from app.utils.keyboard import KeyBoardFactory


async def edit_schedule_step_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = update.callback_query.from_user
    await query.answer()
    base = Core()
    keyboard = KeyBoardFactory(1)
    user_flow_storage[user.id] = {}
    for schedule in base.show_schedules():
        text = f"{schedule.sport}: {schedule.t_start} - {schedule.t_end} {schedule.date}"
        trace_id = uuid.uuid4().hex
        if schedule.participants:
            text += f" Участников:{schedule.participants}"
            keyboard.go_to_new_line()
            keyboard.add_item(text, "jtt_1", trace_id)
            keyboard.go_to_new_line()
        else:
            keyboard.add_item(text, "jtt_1", trace_id)
        user_flow_storage[user.id][trace_id] = schedule.to_dict()
    await query.edit_message_text(text=f"Выберете занятие", reply_markup=keyboard.generate())
    return START_ROUTES


async def edit_schedule_step_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = update.callback_query.from_user
    await query.answer()
    keyboard = KeyBoardFactory()
    flow_info = user_flow_storage[user.id][json.loads(update.callback_query.data)["trace_id"]]
    with Connection() as con:
        repository = SchedulesRepository(con)
        schedules: list[ScheduleModel] = repository.get_all_by_date_and_sport(flow_info["date"], flow_info["sport_id"])
    exist_schedules = {(schedule.t_start, schedule.t_end) for schedule in schedules}
    available_times = [
        f"{hour}:00 - {hour + 1}:00" for hour in range(8, 21) if (f"{hour}:00", f"{hour + 1}:00") not in exist_schedules
    ]
    for item in available_times:
        trace_id = uuid.uuid4().hex
        user_flow_storage[user.id][trace_id] = {}
        user_flow_storage[user.id][trace_id].update(flow_info)
        user_flow_storage[user.id][trace_id]["time"] = item
        keyboard.add_item(item, "es_2", trace_id)
    await query.edit_message_text(text=f"На какое время перенести занятие?", reply_markup=keyboard.generate())
    return START_ROUTES


async def edit_schedule_step_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = update.callback_query.from_user
    await query.answer()
    flow = UserFlowAdmin()
    keyboard = KeyBoardFactory()
    flow_info = user_flow_storage[user.id][json.loads(update.callback_query.data)["trace_id"]]
    time_start, time_end = flow_info["time"].split(" - ")
    flow.edit_schedule(flow_info["id"], flow_info["date"], time_start, time_end)
    await query.edit_message_text(text=f"Расписание успешно изменено", reply_markup=keyboard.generate())
    return END_ROUTES
