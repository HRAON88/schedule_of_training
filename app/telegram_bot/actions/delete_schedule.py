import uuid
import json
from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from app.services.user_flow_admin import UserFlowAdmin
from app.telegram_bot.settings import START_ROUTES, END_ROUTES
from app.user_flow_storage import user_flow_storage
from app.utils.keyboard import KeyBoardFactory


async def delete_schedule_step_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = update.callback_query.from_user
    await query.answer()
    flow = UserFlowAdmin()
    keyboard = KeyBoardFactory(2)
    user_flow_storage[user.id] = {}
    for schedule in flow.show_schedules():
        day = schedule.date
        t_start = schedule.t_start
        t_end = schedule.t_end
        sport = schedule.sport
        text = f"{sport}: {t_start} - {t_end} {day}"
        trace_id = uuid.uuid4().hex
        keyboard.add_item(text, "ds_1", trace_id)
        user_flow_storage[user.id][trace_id] = schedule.to_dict()
    await query.edit_message_text(text=f"Выберете занятие", reply_markup=keyboard.generate())
    return START_ROUTES


async def delete_schedule_step_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = update.callback_query.from_user
    await query.answer()
    flow = UserFlowAdmin()
    keyboard = KeyBoardFactory()
    flow_info = user_flow_storage[user.id][json.loads(update.callback_query.data)["trace_id"]]
    flow.delete_schedule(flow_info["id"])
    await query.edit_message_text(text=f"Расписание успешно удалено", reply_markup=keyboard.generate())
    return END_ROUTES