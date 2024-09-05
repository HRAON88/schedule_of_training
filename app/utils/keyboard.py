from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.schemes.callback_data import CallBackData


class KeyBoardFactory:
    def __init__(self, column_count=4):
        self.column_count = column_count
        self.keyboard = [[]]
        self.default_line = [
            InlineKeyboardButton("Вернуться в меню", callback_data=CallBackData(tag="back_to_menu").model_dump_json())
        ]

    def add_item(self, text: str, tag: str, trace_id: str | None = None):
        last_row = self.keyboard[-1]
        if len(last_row) < self.column_count:
            last_row.append(
                InlineKeyboardButton(text, callback_data=CallBackData(tag=tag, trace_id=trace_id).model_dump_json())
            )
        else:
            self.keyboard.append(
                [InlineKeyboardButton(text, callback_data=CallBackData(tag=tag, trace_id=trace_id).model_dump_json())]
            )

    def add_new_line(self):
        self.keyboard.append([])

    def generate(self):
        last_row = self.keyboard[-1]
        if not last_row:
            self.keyboard.pop(-1)
        self.keyboard.append(self.default_line)
        return InlineKeyboardMarkup(self.keyboard)
