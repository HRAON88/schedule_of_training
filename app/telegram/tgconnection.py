import telebot
from telebot import types

from app.services.core import Core
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
        item1 = types.KeyboardButton("Создать расписание")
        item2 = types.KeyboardButton("Удалить расписание")
        item3 = types.KeyboardButton("Изменить расписание")
        item4 = types.KeyboardButton("Изменить пользователя")
        markup.add(item1, item2, item3, item4)

        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


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


@bot.message_handler(func=lambda message: message.text == "Показать рапсписание")
def book_training(message):
    user_id = message.chat.id
    if user_id in user_trainings:
        bot.send_message(user_id, "Вы уже записаны на тренировку.")
    else:
        user_trainings[user_id] = True
        bot.send_message(user_id, "Вы успешно записаны на тренировку!")


@bot.message_handler(func=lambda message: "Изменить пользователя с id=" in message.text)
def change(message):
    user_id = message.text.split("Изменить пользователя с id=")
    bot.reply_to(message, f"Popka: {user_id}")


# Обработка сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(message.text)
    bot.reply_to(message, "Пожалуйста, используйте кнопки для взаимодействия.")
