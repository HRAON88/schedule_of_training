import telebot
from telebot import types

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
@bot.message_handler(func=lambda message: "Изменить пользователя с id=" in message.text)
def change(message):
    user_id = message.text.split("Изменить пользователя с id=")
    bot.reply_to(message, f"Popka: {user_id}")

@bot.message_handler(func=lambda message: message.text == "Показать расписания" and message.chat.id == 5019406849)
def show_all_schedule(message):
    bot.reply_to(message, f"Всё расписание {UserFlowAdmin().show_all_logs()}")

@bot.message_handler(func=lambda message: "Создать расписание" in message.text and message.chat.id == 5019406849)
def create_schedule(message):
    try:
        format = message.text.lstrip("Создать расписание").split()
        if len(tuple(format)) == 3:
            dtstart = format[0]
            dtend = format[1]
            sportid = format[2]
            UserFlowAdmin().create_schedule(dtstart, dtend, sportid)
            bot.reply_to(message, 'успешно добавлено!')
        else:
            bot.reply_to(message, f'неверный формат данных{tuple(format)}')

    except BaseException as e:
        print('неверный формат данных')
        print(e)



    bot.reply_to(message, 'введите данные в формате: "Создать расписание 10:00/01/01 12:00/01/01 1"')

# Обработка сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(message.text)
    bot.reply_to(message, "Пожалуйста, используйте кнопки для взаимодействия.")
