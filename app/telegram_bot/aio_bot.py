import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler

from app.services.core import Core
from app.settings import settings
from app.telegram_bot.actions.create_schedule import create_schedule_step_1, create_schedule_step_2
from app.telegram_bot.actions.delete_schedule import delete_schedule
from app.telegram_bot.actions.edit_schedule import edit_schedule
from app.telegram_bot.actions.show_allowed_schedules import show_allowed_schedules
from app.telegram_bot.actions.show_my_schedules import show_my_schedules
from app.telegram_bot.actions.start import start
from app.telegram_bot.actions.start_over import start_over
from app.telegram_bot.settings import START_ROUTES, END_ROUTES


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(settings.token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(create_schedule_step_1, pattern="^" + "create_schedule" + "$"),
                CallbackQueryHandler(create_schedule_step_2, pattern="^" + "create_schedule_time_"),
                CallbackQueryHandler(delete_schedule, pattern="^" + "delete_schedule" + "$"),
                CallbackQueryHandler(edit_schedule, pattern="^" + "edit_schedule" + "$"),
                CallbackQueryHandler(edit_schedule, pattern="^" + "edit_user_role" + "$"),
                CallbackQueryHandler(show_my_schedules, pattern="^" + "show_my_schedules" + "$"),
                CallbackQueryHandler(show_allowed_schedules, pattern="^" + "show_allowed_schedules" + "$"),
            ],
            END_ROUTES: [
                CallbackQueryHandler(start_over, pattern="^" + "back_to_menu" + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],

    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)