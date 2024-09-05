import json
import re

from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ConversationHandler

from app.settings import settings
from app.telegram_bot.actions.create_schedule import (
    create_schedule_step_1,
    create_schedule_step_2,
    create_schedule_step_3,
    create_schedule_step_4,
)
from app.telegram_bot.actions.delete_schedule import delete_schedule_step_1, delete_schedule_step_2
from app.telegram_bot.actions.edit_schedule import edit_schedule_step_1, edit_schedule_step_2, edit_schedule_step_3
from app.telegram_bot.actions.edit_user_role import edit_user_role_step_1, edit_user_role_step_2, edit_user_role_step_3
from app.telegram_bot.actions.join_to_training import join_to_training_step_1, join_to_training_step_2
from app.telegram_bot.actions.show_my_schedules import show_my_schedules
from app.telegram_bot.actions.start import start
from app.telegram_bot.actions.start_over import start_over
from app.telegram_bot.settings import END_ROUTES, START_ROUTES


def parse_callback(pattern):
    def validate(callback_data):
        data = json.loads(callback_data)
        tag = data["tag"]
        return re.match(pattern, tag)

    return validate


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(settings.token).build()

    conv_handler = ConversationHandler(
        allow_reentry=True,
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(create_schedule_step_1, pattern=parse_callback("^create_schedule$")),
                CallbackQueryHandler(create_schedule_step_2, pattern=parse_callback("^cs_1$")),
                CallbackQueryHandler(create_schedule_step_3, pattern=parse_callback("^cs_2$")),
                CallbackQueryHandler(create_schedule_step_4, pattern=parse_callback("^cs_3$")),
                CallbackQueryHandler(delete_schedule_step_1, pattern=parse_callback("^delete_schedule$")),
                CallbackQueryHandler(delete_schedule_step_2, pattern=parse_callback("^ds_1$")),
                CallbackQueryHandler(edit_schedule_step_1, pattern=parse_callback("^edit_schedule$")),
                CallbackQueryHandler(edit_schedule_step_2, pattern=parse_callback("^es_1")),
                CallbackQueryHandler(edit_schedule_step_3, pattern=parse_callback("^es_2")),
                CallbackQueryHandler(edit_user_role_step_1, pattern=parse_callback("^edit_user_role$")),
                CallbackQueryHandler(edit_user_role_step_2, pattern=parse_callback("^eur_1$")),
                CallbackQueryHandler(edit_user_role_step_3, pattern=parse_callback("^eur_2$")),
                CallbackQueryHandler(show_my_schedules, pattern=parse_callback("^show_my_schedules$")),
                CallbackQueryHandler(join_to_training_step_1, pattern=parse_callback("^join_to_training$")),
                CallbackQueryHandler(join_to_training_step_2, pattern=parse_callback("^jtt_1$")),
                CallbackQueryHandler(start_over, pattern=parse_callback("back_to_menu")),
            ],
            END_ROUTES: [
                CallbackQueryHandler(start_over, pattern=parse_callback("back_to_menu")),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
