import json
import uuid

from telegram import Update
from telegram.ext import ContextTypes

from app.database.models.schedules import ScheduleModel
from app.services.core import Core
from app.telegram_bot.settings import START_ROUTES, END_ROUTES
from app.user_flow_storage import user_flow_storage
from app.utils.keyboard import KeyBoardFactory


async def join_to_training_step_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = update.callback_query.from_user
    await query.answer()
    base = Core()
    keyboard = KeyBoardFactory(2)
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
        user_flow_storage[user.id][trace_id] = {"schedule": schedule.to_dict()}
    await query.edit_message_text(text=f"Выберете занятие", reply_markup=keyboard.generate())
    return START_ROUTES


async def join_to_training_step_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    tg_user = update.callback_query.from_user
    base = Core()
    user = base.get_user(tg_user.id)
    await query.answer()
    keyboard = KeyBoardFactory()
    flow_info = user_flow_storage[user.id][json.loads(update.callback_query.data)["trace_id"]]
    schedule = ScheduleModel(**flow_info["schedule"])
    base.join_to_train(user.id, schedule.id)
    await query.edit_message_text(text=f"Вы успешно присоединились к тренировке", reply_markup=keyboard.generate())
    return END_ROUTES
