import telebot
from telebot import types
from telebot.types import User

from app.database.repository.users import UsersRepository
from app.services.core import Core
from app.services.user_flow_admin import UserFlowAdmin
from app.settings import settings

bot = telebot.TeleBot(settings.token)

# Хранение данных о записях
user_trainings = {}


# Начало диалога
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    core = Core()
    bot.reply_to(message, "Добро пожаловать! Нажмите на кнопку, чтобы записаться на тренировку.")
    user = core.get_user(message.chat.id)
    if not user and core.is_admin_mode():
        user = core.add_admin_user(message.chat.id, message.chat.first_name, message.chat.last_name)
    elif not user:
        user = core.add_basic_user(message.chat.id, message.chat.first_name, message.chat.last_name)

    if user.is_admin():
        # Создание кнопки для спортсмена
        markup = types.ReplyKeyboardMarkup(row_width=3)
        item1 = types.KeyboardButton("Записаться на тренировку")
        item2 = types.KeyboardButton("Отказаться от тренировки")
        item3 = types.KeyboardButton("Показать расписание")
        markup.add(item1, item2, item3)

        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(row_width=4)
        item0 = types.KeyboardButton("Показать расписания")
        item1 = types.KeyboardButton("Создать расписание")
        item2 = types.KeyboardButton("Удалить расписание")
        item3 = types.KeyboardButton("Изменить расписание")
        item4 = types.KeyboardButton("Изменить пользователя")
        markup.add(item0, item1, item2, item3, item4)

        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

#кнопки спортсмена
# Запись на тренировку
@bot.message_handler(func=lambda message: message.text == "Записаться на тренировку")
def book_training(message):
    user_id = message.chat.id
    if user_id in user_trainings:
        bot.send_message(user_id, "Вы уже записаны на тренировку.")
    else:
        user_trainings[user_id] = True
        bot.send_message(user_id, "Вы успешно записаны на тренировку!")


# Отказ от тренировки
@bot.message_handler(func=lambda message: message.text == "Отказаться от тренировки")
def cancel_training(message):
    user_id = message.chat.id
    if user_id in user_trainings:
        del user_trainings[user_id]
        bot.send_message(user_id, "Вы успешно отказались от тренировки.")
    else:
        bot.send_message(user_id, "Вы не записаны на тренировку.")


@bot.message_handler(func=lambda message: message.text == "Показать расписание")
def book_training(message):
    user_id = message.chat.id
    if user_id in user_trainings:
        bot.send_message(user_id, "Вы уже записаны на тренировку.")
    else:
        user_trainings[user_id] = True
        bot.send_message(user_id, "Вы успешно записаны на тренировку!")

#кнопки админа
@bot.message_handler(func=lambda message: message.text == "Изменить пользователя")
def change(message):
    msg = bot.reply_to(message, f"выберите какого пользователя хотите изменить: {UserFlowAdmin().show_all_users_by_admin()}")
    bot.register_next_step_handler(msg, process_edit_user)

def process_edit_user(message):
    msg = bot.reply_to(message, "напишите должность выбранного пользователя admin, coach, sportsman")

    global change_id
    change_id = message.text
    bot.register_next_step_handler(msg, process_edit_user_step)

def process_edit_user_step(message):
    global change_id
    UserFlowAdmin().change_user_role(id_outer=change_id, role_id_user=message.text)
    bot.reply_to(message, "успешно изменено!")
@bot.message_handler(func=lambda message: message.text == "Показать расписания" and message.chat.id == 5019406849)
def show_all_schedule(message):
    bot.reply_to(message, f"Всё расписание {UserFlowAdmin().show_all_schedules()}")

@bot.message_handler(func=lambda message: "Создать расписание" in message.text and message.chat.id == 5019406849)
def create_schedule(message):
    msg = bot.reply_to(message, 'введите начало времени занятия в формате ЧЧ:ММ/ЧЧ.ММ')
    bot.register_next_step_handler(msg, process_dtstart_step)
    global new_schedule
    new_schedule = []
def process_dtstart_step(message):
    if len(message.text) == 11:
        new_schedule.append(message.text)
        msg = bot.reply_to(message, 'введите окончание времени занятия в формате ЧЧ:ММ/ЧЧ.ММ')
        bot.register_next_step_handler(msg, process_dtend_step)
    else:
        msg = bot.reply_to(message, 'введите начало времени занятия в формате ЧЧ:ММ/ЧЧ.ММ')
        bot.register_next_step_handler(msg, process_dtstart_step)
def process_dtend_step(message):
    if len(message.text) == 11:
        new_schedule.append(message.text)
        msg = bot.reply_to(message, 'введите id названия спорта')
        bot.register_next_step_handler(msg, process_sportid_step)
    else:
        msg = bot.reply_to(message, 'введите окончание времени занятия в формате ЧЧ:ММ/ЧЧ.ММ')
        bot.register_next_step_handler(msg, process_dtend_step)

def process_sportid_step(message):
    if len(message.text) == 1:
        new_schedule.append(message.text)

    if len(new_schedule) == 3:
        dtstart = new_schedule[0]
        dtend = new_schedule[1]
        sportid = int(new_schedule[2])
        UserFlowAdmin().create_schedule(dtstart, dtend, sportid)
        bot.reply_to(message, f'успешно добавлено! начало - {dtstart}, конец - {dtend}, спорт id - {sportid}')
    else:
        bot.reply_to(message, f'что-то пошло не так. попробуйте ещё раз')



    bot.reply_to(message, 'введите данные в формате: "Создать расписание 10:00/01/01 12:00/01/01 1"')

@bot.message_handler(func=lambda message: message.text == "Удалить расписание" and message.chat.id == 5019406849)
def delete_schedule(message):
    msg = bot.reply_to(message, 'введите id расписания')
    bot.register_next_step_handler(msg, process_delete_schedule)
def process_delete_schedule(message):
    if int(message.text):
        UserFlowAdmin().delete_schedule(message.text)
        bot.reply_to(message, 'успешно удалено!')
    else:
        msg = bot.reply_to(message, 'введите корректный id расписания')
        bot.register_next_step_handler(msg, process_delete_schedule)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(message.text)
    bot.reply_to(message, "Пожалуйста, используйте кнопки для взаимодействия.")
