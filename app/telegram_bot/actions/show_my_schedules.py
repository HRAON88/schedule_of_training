import json
import uuid

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.schemes.callback_data import CallBackData
from app.services.core import Core
from app.telegram_bot.settings import END_ROUTES, START_ROUTES
from app.user_flow_storage import user_flow_storage
from app.utils.keyboard import KeyBoardFactory


async def show_my_schedules_step_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = update.callback_query.from_user
    await query.answer()
    base = Core()
    keyboard = KeyBoardFactory(2)
    user_flow_storage[user.id] = {}
    user_schedules = {logs.schedule_id for logs in base.get_schedules_by_user(user.id)}
    for schedule in base.show_schedules():
        if schedule.id not in user_schedules:
            continue
        text = f"{schedule.sport}: {schedule.t_start} - {schedule.t_end} {schedule.date} Участников:{schedule.participants}"
        trace_id = uuid.uuid4().hex
        keyboard.go_to_new_line()
        keyboard.add_item(text, "sms_1", trace_id)
        keyboard.go_to_new_line()
        user_flow_storage[user.id][trace_id] = {"schedule": schedule.to_dict(), "user": base.get_user(user.id).to_dict()}
    await query.edit_message_text(text=f"Выберете тренировку для взаимодействия с ней", reply_markup=keyboard.generate())
    return START_ROUTES


async def show_my_schedules_step_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = update.callback_query.from_user
    await query.answer()
    keyboard = KeyBoardFactory()
    flow_info = user_flow_storage[user.id][json.loads(update.callback_query.data)["trace_id"]]
    for action in ["Отказаться", "Показать участников"]:
        trace_id = uuid.uuid4().hex
        keyboard.add_item(action, "sms_2", trace_id)
        user_flow_storage[user.id][trace_id] = {"action": action}
        user_flow_storage[user.id][trace_id].update(flow_info)
    await query.edit_message_text(text=f"Выберете действие", reply_markup=keyboard.generate())
    return START_ROUTES


async def show_my_schedules_step_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = update.callback_query.from_user
    await query.answer()
    keyboard = KeyBoardFactory()
    base = Core()
    flow_info = user_flow_storage[user.id][json.loads(update.callback_query.data)["trace_id"]]
    actions = {
        "Отказаться": (base.refuse_to_train, lambda x: {"user_id": x["user"]["id"], "schedule_id": x["schedule"]["id"]}),
        "Показать участников": (base.get_participants, lambda x: {"schedule_id": x["schedule"]["id"]})
    }
    handler, get_attr_func = actions[flow_info["action"]]
    kwargs = get_attr_func(flow_info)
    result = handler(**kwargs)
    if result:
        for item in result:
            keyboard.add_item(item.to_str(), "sms_3")
    await query.edit_message_text(text=f"Готово!", reply_markup=keyboard.generate())
    return END_ROUTES
