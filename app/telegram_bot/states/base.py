import json
import uuid
from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import ContextTypes

from app.telegram_bot.settings import logger
from app.user_flow_storage import user_flow_storage


class State(ABC):
    state = None

    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.update = update
        self.bot_context = context
        self.query = self.update.callback_query
        self.message = self.update.message
        if self.query:
            self.user = update.callback_query.from_user
        else:
            self.user = update.message.from_user
        logger.info(f"{self.user} in state: {self.state}")

    @abstractmethod
    async def run(self):
        pass

    def get_context(self):
        trace_id = json.loads(self.query.data).get("trace_id")
        if trace_id:
            return user_flow_storage[self.user.id][trace_id]
        if self.user.id not in user_flow_storage:
            user_flow_storage[self.user.id] = {}
        return user_flow_storage[self.user.id]

    def set_context(self, trace_id: str, data: dict) -> None:
        old_context = self.get_context()
        if self.user.id not in user_flow_storage:
            user_flow_storage[self.user.id] = {}
        if trace_id not in user_flow_storage[self.user.id]:
            user_flow_storage[self.user.id][trace_id] = {}
            user_flow_storage[self.user.id][trace_id].update(old_context)

        user_flow_storage[self.user.id][trace_id].update(**data)

    @staticmethod
    def create_trace_id():
        return uuid.uuid4().hex[:10]
