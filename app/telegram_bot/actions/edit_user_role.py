import uuid
import json
from telegram import Update
from telegram.ext import ContextTypes

from app.services.core import Core
from app.services.user_flow_admin import UserFlowAdmin
from app.telegram_bot.settings import START_ROUTES, END_ROUTES
from app.user_flow_storage import user_flow_storage
from app.utils.keyboard import KeyBoardFactory


async def edit_user_role_step_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    tg_user = update.callback_query.from_user
    await query.answer()
    flow = UserFlowAdmin()
    core = Core()
    roles = core.get_roles()
    roles = {role.id: role for role in roles}
    keyboard = KeyBoardFactory(2)
    user_flow_storage[tg_user.id] = {}
    for user in flow.get_users():
        text = roles[user.role_id].role
        if user.lastname and user.lastname.strip() not in ("null", ""):
            text += f" {user.lastname}"
        if user.firstname and user.firstname.strip() not in ("null", ""):
            text += f" {user.firstname}"
        if user.username and user.username.strip() not in ("null", ""):
            text += f" ({user.username})"
        trace_id = uuid.uuid4().hex
        keyboard.add_item(text, "eur_1", trace_id)
        user_flow_storage[tg_user.id][trace_id] = {"user": user.to_dict()}
    await query.edit_message_text(text=f"Выберете пользователя", reply_markup=keyboard.generate())
    return START_ROUTES


async def edit_user_role_step_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = update.callback_query.from_user
    await query.answer()
    core = Core()
    keyboard = KeyBoardFactory()
    flow_info = user_flow_storage[user.id][json.loads(update.callback_query.data)["trace_id"]]
    for role in core.get_roles():
        trace_id = uuid.uuid4().hex
        keyboard.add_item(role.role, "eur_2", trace_id)
        user_flow_storage[user.id][trace_id] = {"role": role.to_dict()}
        user_flow_storage[user.id][trace_id].update(flow_info)
    await query.edit_message_text(text=f"Выберете роль", reply_markup=keyboard.generate())
    return START_ROUTES

async def edit_user_role_step_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = update.callback_query.from_user
    await query.answer()
    flow = UserFlowAdmin()
    keyboard = KeyBoardFactory()
    flow_info = user_flow_storage[user.id][json.loads(update.callback_query.data)["trace_id"]]
    flow.change_user_role(flow_info["user"]["id"], flow_info["role"]["id"])
    await query.edit_message_text(text=f"Пользователь получил роль '{flow_info['role']['role']}'", reply_markup=keyboard.generate())
    return END_ROUTES