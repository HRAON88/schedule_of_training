import json
import re
from typing import Type

from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ConversationHandler, ContextTypes

from app.settings import settings

from app.telegram_bot.settings import END_ROUTES, START_ROUTES
from app.telegram_bot.states.start import Start
from app.telegram_bot.states.base import State
from app.telegram_bot.states.choose_date import ChooseDate
from app.telegram_bot.states.choose_sport import ChooseSport
from app.telegram_bot.states.choose_user_role import ChooseUserRole
from app.telegram_bot.states.create_schedule import CreateSchedule
from app.telegram_bot.states.delete_schedule import DeleteSchedule
from app.telegram_bot.states.edit_schedule import EditSchedule
from app.telegram_bot.states.edit_user_role import EditUserRole
from app.telegram_bot.states.join_to_training import JoinToTraining
from app.telegram_bot.states.refuse_to_train import RefuseToTrain
from app.telegram_bot.states.show_actions_with_schedules import ShowActionsWithSchedules, ShowActionsWithMySchedules
from app.telegram_bot.states.show_all_users import ShowAllUsers
from app.telegram_bot.states.show_allowed_times import ShowAllowedTimesForEdit, ShowAllowedTimesForCreate
from app.telegram_bot.states.show_my_schedules import ShowMySchedules
from app.telegram_bot.states.show_participants import ShowParticipants
from app.telegram_bot.states.show_schedules import ShowSchedules


def parse_callback(pattern):
    def validate(callback_data):
        data = json.loads(callback_data)
        tag = data["tag"]
        return re.match(pattern, tag)

    return validate


def set_state(state: Type[State]):
    async def call_state(update: Update, context: ContextTypes.DEFAULT_TYPE):
        return await state(update, context).run()

    return call_state


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(settings.token).build()

    conv_handler = ConversationHandler(
        allow_reentry=True,
        entry_points=[CommandHandler("start", set_state(Start))],
        states={
            START_ROUTES: [
                CallbackQueryHandler(set_state(ShowAllUsers), pattern=parse_callback(ShowAllUsers.state)),
                CallbackQueryHandler(set_state(ShowMySchedules), pattern=parse_callback(ShowMySchedules.state)),
                CallbackQueryHandler(set_state(ShowSchedules), pattern=parse_callback(ShowSchedules.state)),
                CallbackQueryHandler(set_state(ChooseDate), pattern=parse_callback(ChooseDate.state)),
                CallbackQueryHandler(set_state(Start), pattern=parse_callback(Start.state)),
            ],
            END_ROUTES: [
                CallbackQueryHandler(set_state(Start), pattern=parse_callback(Start.state)),
            ],
            ShowSchedules.state: [
                CallbackQueryHandler(set_state(ShowActionsWithSchedules), pattern=parse_callback(ShowActionsWithSchedules.state)),
                CallbackQueryHandler(set_state(Start), pattern=parse_callback(Start.state)),
            ],
            ShowActionsWithSchedules.state: [
                CallbackQueryHandler(set_state(DeleteSchedule), pattern=parse_callback(DeleteSchedule.state)),
                CallbackQueryHandler(set_state(ShowAllowedTimesForEdit), pattern=parse_callback(ShowAllowedTimesForEdit.state)),
                CallbackQueryHandler(set_state(JoinToTraining), pattern=parse_callback(JoinToTraining.state)),
                CallbackQueryHandler(set_state(Start), pattern=parse_callback(Start.state)),
            ],
            ShowAllowedTimesForEdit.state: [
                CallbackQueryHandler(set_state(EditSchedule), pattern=parse_callback(EditSchedule.state)),
                CallbackQueryHandler(set_state(Start), pattern=parse_callback(Start.state)),
            ],
            ChooseDate.state: [
                CallbackQueryHandler(set_state(ChooseSport), pattern=parse_callback(ChooseSport.state)),
                CallbackQueryHandler(set_state(Start), pattern=parse_callback(Start.state)),
            ],
            ChooseSport.state: [
                CallbackQueryHandler(set_state(ShowAllowedTimesForCreate), pattern=parse_callback(ShowAllowedTimesForCreate.state)),
                CallbackQueryHandler(set_state(Start), pattern=parse_callback(Start.state)),
            ],
            ShowAllowedTimesForCreate.state: [
                CallbackQueryHandler(set_state(CreateSchedule), pattern=parse_callback(CreateSchedule.state)),
                CallbackQueryHandler(set_state(Start), pattern=parse_callback(Start.state)),
            ],
            ShowMySchedules.state: [
                CallbackQueryHandler(set_state(ShowActionsWithMySchedules), pattern=parse_callback(ShowActionsWithMySchedules.state)),
                CallbackQueryHandler(set_state(Start), pattern=parse_callback(Start.state)),
            ],
            ShowActionsWithMySchedules.state: [
                CallbackQueryHandler(set_state(ShowParticipants), pattern=parse_callback(ShowParticipants.state)),
                CallbackQueryHandler(set_state(RefuseToTrain), pattern=parse_callback(RefuseToTrain.state)),
                CallbackQueryHandler(set_state(Start), pattern=parse_callback(Start.state)),
            ],
            ShowAllUsers.state: [
                CallbackQueryHandler(set_state(ChooseUserRole), pattern=parse_callback(ChooseUserRole.state)),
                CallbackQueryHandler(set_state(Start), pattern=parse_callback(Start.state)),
            ]
            ,
            ChooseUserRole.state: [
                CallbackQueryHandler(set_state(EditUserRole), pattern=parse_callback(EditUserRole.state)),
                CallbackQueryHandler(set_state(Start), pattern=parse_callback(Start.state)),
            ]
        },
        fallbacks=[CommandHandler("start", set_state(Start))],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
