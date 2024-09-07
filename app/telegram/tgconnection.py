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
    print(message)
    core = Core()
    tg_user = message.from_user
    user = core.get_user(tg_user.id)

    if not user and core.is_admin_mode():
        user = core.add_admin_user(tg_user.id, tg_user.first_name, tg_user.last_name, tg_user.username)
    elif not user:
        user = core.add_basic_user(tg_user.id, tg_user.first_name, tg_user.last_name, tg_user.username)

    if not user.is_admin():
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
@bot.message_handler(func=lambda message: message.text == "Записаться на тренировку" and Core().get_user(message.chat.id).is_sportsman())
def book_training(message):
    user_id = message.chat.id
    if user_id in user_trainings:
        bot.send_message(user_id, "Вы уже записаны на тренировку.")
    else:
        user_trainings[user_id] = True
        bot.send_message(user_id, "Вы успешно записаны на тренировку!")


# Отказ от тренировки
@bot.message_handler(func=lambda message: message.text == "Отказаться от тренировки" and Core().get_user(message.chat.id).is_sportsman())
def cancel_training(message):
    user_id = message.chat.id
    if user_id in user_trainings:
        del user_trainings[user_id]
        bot.send_message(user_id, "Вы успешно отказались от тренировки.")
    else:
        bot.send_message(user_id, "Вы не записаны на тренировку.")


@bot.message_handler(func=lambda message: message.text == "Показать расписание" and Core().get_user(message.chat.id).is_sportsman())
def book_training(message):
    user_id = message.chat.id
    if user_id in user_trainings:
        bot.send_message(user_id, "Вы уже записаны на тренировку.")
    else:
        user_trainings[user_id] = True
        bot.send_message(user_id, "Вы успешно записаны на тренировку!")

#кнопки админа
@bot.message_handler(func=lambda message: message.text == "Изменить пользователя" and Core().get_user(message.chat.id).is_admin())
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
    dict_with_roles = {'admin':1, 'coach':2, 'sportsman':3}
    try:
        UserFlowAdmin().change_user_role(change_id, dict_with_roles[message.text])
        bot.reply_to(message, "успешно изменено! Необходимо обновить бота")
    except BaseException:
        bot.reply_to(message, "Попробуйте сначала")

@bot.message_handler(func=lambda message: message.text == "Показать расписания" and message.chat.id == 5019406849)
def show_all_schedule(message):
    bot.reply_to(message, f"Всё расписание {UserFlowAdmin().show_all_schedules()}")

@bot.message_handler(func=lambda message: "Создать расписание" in message.text and Core().get_user(message.chat.id).is_admin())
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






@bot.message_handler(func=lambda message: "Изменить раписание" in message.text and Core().get_user(message.chat.id).is_admin())
def edit_schedule_step1(message):
    msg = bot.reply_to(message, f'Введите id расписания, которое хотите изменить {UserFlowAdmin().show_all_schedules()}')
    bot.register_next_step_handler(msg, process_edit_schedule_step2)
def process_edit_schedule_step2(message):
    global schedule_changed_id
    schedule_changed_id = message.text

    try:

        markup = types.ReplyKeyboardMarkup(row_width=3)
        item1 = types.KeyboardButton("Начало тренировки")
        item2 = types.KeyboardButton("Конец тренировки")
        item3 = types.KeyboardButton("Спорт id")
        markup.add(item1, item2, item3)
        msg = bot.reply_to(message, "укажите что хотите изменить", reply_markup=markup)
        bot.register_next_step_handler(msg, process_edit_schedule_step3)
    except:

        markup = types.ReplyKeyboardMarkup(row_width=4)
        item0 = types.KeyboardButton("Показать расписания")
        item1 = types.KeyboardButton("Создать расписание")
        item2 = types.KeyboardButton("Удалить расписание")
        item3 = types.KeyboardButton("Изменить расписание")
        item4 = types.KeyboardButton("Изменить пользователя")
        markup.add(item0, item1, item2, item3, item4)
        bot.reply_to(message, "Попробуйте ещё раз", reply_markup=markup)

def process_edit_schedule_step3(message):
    if message.text == "Начало тренировки":
        msg = bot.reply_to(message, "Напишите новое время начала тренировки")
        bot.register_next_step_handler(msg, process_edit_schedule_step3_start)







def process_edit_schedule_step3_start(message):
    UserFlowAdmin().edit_schedule(id_outer=schedule_changed_id,dtstart_user=message.text)
    bot.reply_to(message, 'успешно изменено!')


@bot.message_handler(func=lambda message: message.text == "Удалить расписание" and Core().get_user(message.chat.id).is_admin())
def delete_schedule(message):

    msg = bot.reply_to(message, 'введите id расписания')
    bot.register_next_step_handler(msg, process_delete_schedule)
def process_delete_schedule(message):
    try:
        if int(message.text):

            UserFlowAdmin().delete_schedule(message.text)
            bot.reply_to(message, 'успешно удалено!')

            bot.reply_to(message, 'Попробуйте еще раз')

        else:
            msg = bot.reply_to(message, 'введите корректный id расписания')
            bot.register_next_step_handler(msg, process_delete_schedule)
    except BaseException:
        bot.reply_to(message, 'Попробуйте еще раз')
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(message.text)
    bot.reply_to(message, "Пожалуйста, используйте кнопки для взаимодействия.")
