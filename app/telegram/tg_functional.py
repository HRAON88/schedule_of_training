import telebot
from telebot import types
from telebot.types import User

from app.database.repository.users import UsersRepository
from app.services.core import Core
from app.services.user_flow_admin import UserFlowAdmin
from app.services.user_flow_coach import UserFlowCoach
from app.services.user_flow_sportsman import UserFlowSportsman
from app.settings import settings

bot = telebot.TeleBot(settings.token)

# Хранение данных о записях
user_trainings = {}


# Начало диалога
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Для взаимодействия используйте кнопки!")
    core = Core()
    tg_user = message.from_user
    user = core.get_user(tg_user.id)
    if not user and core.is_admin_mode():
        user = core.add_admin_user(tg_user.id, tg_user.first_name, tg_user.last_name, tg_user.username)
    elif not user:
        user = core.add_basic_user(tg_user.id, tg_user.first_name, tg_user.last_name, tg_user.username)

    if user.is_coach():
        main_menu_for_coach(message.chat.id)
    elif user.is_sportsman():
        main_menu_for_sportsman(message.chat.id)
    elif user.is_admin():
        main_menu_for_admin(message.chat.id)

def main_menu_for_coach(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    item1 = types.KeyboardButton("Показать кто идёт")
    markup.add(item1)
    bot.send_message(message, 'Главное меню', reply_markup=markup)

def main_menu_for_sportsman(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    item1 = types.KeyboardButton("Записаться на тренировку")
    item2 = types.KeyboardButton("Отказаться от тренировки")
    item3 = types.KeyboardButton("Показать расписание")
    markup.add(item1, item2, item3)
    bot.send_message(message, 'Главное меню', reply_markup=markup)
def main_menu_for_admin(message):
    markup = types.ReplyKeyboardMarkup(row_width=4)
    item0 = types.KeyboardButton("Показать расписания")
    item1 = types.KeyboardButton("Создать расписание")
    item2 = types.KeyboardButton("Удалить расписание")
    item3 = types.KeyboardButton("Изменить расписание")
    item4 = types.KeyboardButton("Изменить пользователя")
    markup.add(item0, item1, item2, item3, item4)
    bot.send_message(message, 'Главное меню', reply_markup=markup)

def cancel_for_admin(message):
    markup = types.ReplyKeyboardMarkup(row_width=4)
    item0 = types.KeyboardButton("Показать расписания")
    item1 = types.KeyboardButton("Создать расписание")
    item2 = types.KeyboardButton("Удалить расписание")
    item3 = types.KeyboardButton("Изменить расписание")
    item4 = types.KeyboardButton("Изменить пользователя")
    markup.add(item0, item1, item2, item3, item4)
    bot.send_message(message, 'Вы возвращены в главное меню', reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == "Показать кто идёт" and Core().get_user(message.chat.id).is_coach())
def show_users_for_coach(message):
    schedules = UserFlowAdmin().show_all_schedules()
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = []
    for count in schedules:
        buttons.append(types.InlineKeyboardButton(text=f"{count}", callback_data=f"т{count[:count.find(')')]}"))
    markup.add(*buttons)
    bot.reply_to(message, 'Выберите из списка тренировок', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Записаться на тренировку" and Core().get_user(message.chat.id).is_sportsman())
def book_training(message):
    schedules = UserFlowAdmin().show_all_schedules()
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = []
    for count in schedules:
        buttons.append(types.InlineKeyboardButton(text=f"{count}", callback_data=f"д{count[:count.find(')')]}"))
    markup.add(*buttons)
    bot.reply_to(message, 'Доступный список тренировок', reply_markup=markup)
@bot.callback_query_handler(func=lambda callback: callback)
def all_call_back(callback):
    if callback.data[0] == 'д':
        book_training(callback)
    elif callback.data[0] == 'у':
        cancel_training_callback(callback)
    elif callback.data[0] == 'т':
        show_count_users(callback)

def show_count_users(callback):
    users = UserFlowCoach().show_users(callback.data[1:])
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = []
    for count in users:
        buttons.append(types.InlineKeyboardButton(text=f"{count[:count.find('@')]}", url=f"https://t.me/{count[count.find('@')+1:]}"))
    markup.add(*buttons)
    bot.send_message(callback.message.chat.id, 'Список участников', reply_markup=markup)

def book_training(callback):
    #bot.send_message(callback.message.chat.id, callback.data)
    result = UserFlowSportsman().join_to_train(user_id=callback.message.chat.id, schedule_id=callback.data[1:])
    if result:
        bot.send_message(callback.message.chat.id, f'Вы успешно записаны!')
        return
    else:
        bot.send_message(callback.message.chat.id, f'Вы уже записаны!')
        return
# @bot.message_handler(func=lambda message: message.text == "17" and Core().get_user(message.chat.id).is_sportsman())
# def cancel_training1(message):
#     UserFlowSportsman().refuse_to_train(users_id=message.chat.id, schedule_id=message.text)



# Отказ от тренировки
@bot.message_handler(func=lambda message: message.text == "Отказаться от тренировки" and Core().get_user(message.chat.id).is_sportsman())
def cancel_training(message):
    schedules = UserFlowSportsman().show_all_booked_schedules(message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = []
    if schedules:
        for count in schedules:
            buttons.append(types.InlineKeyboardButton(text=f"{count[:count.find('+')]}", callback_data=f"у{count[count.find('+'):]}"))
        markup.add(*buttons)
        bot.reply_to(message, f'Ваши тренировки:', reply_markup=markup)
    else:
        bot.reply_to(message, f'У вас еще нет записей! ', reply_markup=markup)


#
def cancel_training_callback(callback):
    result = UserFlowSportsman().refuse_to_train(id=callback.data[1:])
    if result:
        bot.send_message(callback.message.chat.id, f'Запись отменена!')
        return
    else:
        bot.send_message(callback.message.chat.id, f'Запись уже отменена!')
        return

@bot.message_handler(func=lambda message: message.text == "Показать расписание" and Core().get_user(message.chat.id).is_sportsman())
def show_training(message):
    result = UserFlowSportsman().show_all_booked_schedules(message.chat.id)
    if result:
        spis = [count[:count.find('+')] for count in result]
        bot.reply_to(message, "\n".join(spis))
    else:
        bot.reply_to(message, "Вы еще не записаны!")



#кнопки админа
@bot.message_handler(func=lambda message: message.text == "Изменить пользователя" and Core().get_user(message.chat.id).is_admin())
def change(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    item1 = types.KeyboardButton("Отмена")
    markup.add(item1)
    msg = bot.reply_to(message, f"выберите какого пользователя хотите изменить: {UserFlowAdmin().show_all_users_by_admin()}", reply_markup=markup)
    bot.register_next_step_handler(msg, process_edit_user)

def process_edit_user(message):
    if message.text == 'Отмена':
        cancel_for_admin(message.chat.id)
        return
    markup = types.ReplyKeyboardMarkup(row_width=4)
    item1 = types.KeyboardButton("admin")
    item2 = types.KeyboardButton("coach")
    item3 = types.KeyboardButton("sportsman")
    item4 = types.KeyboardButton("Отмена")
    markup.add(item1, item2, item3, item4)

    msg = bot.reply_to(message, "выберите должность пользователя 'admin, coach, sportsman'", reply_markup=markup)

    global change_id
    change_id = message.text
    bot.register_next_step_handler(msg, process_edit_user_step)

def process_edit_user_step(message):
    if message.text == 'Отмена':
        cancel_for_admin(message.chat.id)
        return
    global change_id
    dict_with_roles = {'admin':1, 'coach':2, 'sportsman':3}
    try:
        UserFlowAdmin().change_user_role(change_id, dict_with_roles[message.text])
        bot.reply_to(message, "успешно изменено! Необходимо обновить бота")
        main_menu_for_admin(message.chat.id)
    except BaseException:
        bot.reply_to(message, "Попробуйте сначала")
        main_menu_for_admin(message.chat.id)

@bot.message_handler(func=lambda message: message.text == "Показать расписания" and Core().get_user(message.chat.id).is_admin())
def show_all_schedule(message):
    bot.reply_to(message, f"Всё расписание: \n{UserFlowAdmin().show_all_schedules()}")

@bot.message_handler(func=lambda message: message.text == "Создать расписание" and Core().get_user(message.chat.id).is_admin())
def create_schedule(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    item1 = types.KeyboardButton("Отмена")
    markup.add(item1)
    msg = bot.reply_to(message, 'введите начала времени занятия в формате ЧЧ:ММ/ЧЧ.ММ', reply_markup=markup)
    bot.register_next_step_handler(msg, process_dtstart_step)
    global new_schedule
    new_schedule = []


def process_dtstart_step(message):
    if message.text == 'Отмена':
        cancel_for_admin(message.chat.id)
        return
    if len(message.text) == 11:
        new_schedule.append(message.text)
        markup = types.ReplyKeyboardMarkup(row_width=1)
        item1 = types.KeyboardButton("Отмена")
        markup.add(item1)
        msg = bot.reply_to(message, 'введите окончание времени занятия в формате ЧЧ:ММ/ЧЧ.ММ', reply_markup=markup)
        bot.register_next_step_handler(msg, process_dtend_step)
    else:
        msg = bot.reply_to(message, 'введите начало времени занятия в формате ЧЧ:ММ/ЧЧ.ММ')
        bot.register_next_step_handler(msg, process_dtstart_step)
def process_dtend_step(message):
    if message.text == 'Отмена':
        cancel_for_admin(message.chat.id)
        return
    if len(message.text) == 11:
        new_schedule.append(message.text)
        msg = bot.reply_to(message, 'введите id названия спорта')
        bot.register_next_step_handler(msg, process_sportid_step)
    else:
        msg = bot.reply_to(message, 'введите окончание времени занятия в формате ЧЧ:ММ/ЧЧ.ММ')
        bot.register_next_step_handler(msg, process_dtend_step)

def process_sportid_step(message):
    if message.text == 'Отмена':
        cancel_for_admin(message.chat.id)
        return
    if len(message.text) == 1:
        new_schedule.append(message.text)

    if len(new_schedule) == 3:
        dtstart = new_schedule[0]
        dtend = new_schedule[1]
        sportid = int(new_schedule[2])
        UserFlowAdmin().create_schedule(dtstart, dtend, sportid)
        bot.reply_to(message, f'успешно добавлено! начало - {dtstart}, конец - {dtend}, спорт id - {sportid}')
        main_menu_for_admin(message.chat.id)
    else:
        bot.reply_to(message, f'что-то пошло не так. попробуйте ещё раз')
        cancel_for_admin(message.chat.id)
        return






@bot.message_handler(func=lambda message: message.text == "Изменить расписание"  and Core().get_user(message.chat.id).is_admin())
def edit_schedule_step1(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    item1 = types.KeyboardButton("Отмена")
    markup.add(item1)
    msg = bot.reply_to(message, f'Введите id расписания, которое хотите изменить {UserFlowAdmin().show_all_schedules()}', reply_markup=markup)
    bot.register_next_step_handler(msg, process_edit_schedule_step2)
def process_edit_schedule_step2(message):
    global schedule_changed_id
    schedule_changed_id = message.text

    try:

        markup = types.ReplyKeyboardMarkup(row_width=4)
        item1 = types.KeyboardButton("Начало тренировки")
        item2 = types.KeyboardButton("Конец тренировки")
        item3 = types.KeyboardButton("Спорт id")
        item4 = types.KeyboardButton("Отмена")
        markup.add(item1, item2, item3, item4)
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
    if message.text == 'Отмена':
        cancel_for_admin(message.chat.id)
        return
    if message.text == "Начало тренировки":
        msg = bot.reply_to(message, "Напишите новое время начала тренировки")
        bot.register_next_step_handler(msg, process_edit_schedule_step3_start)
    elif message.text == "Конец тренировки":
        msg = bot.reply_to(message, "Напишите новое время конца тренировки")
        bot.register_next_step_handler(msg, process_edit_schedule_step3_end)
    elif message.text == "Спорт id":
        msg = bot.reply_to(message, "Напишите спорт id")
        bot.register_next_step_handler(msg, process_edit_schedule_step3_id)
    else:
        bot.reply_to(message, 'Используйте кнопки для взаимодействия')
        cancel_for_admin(message.chat.id)
        return


def process_edit_schedule_step3_id(message):
    UserFlowAdmin().edit_schedule(id_outer=schedule_changed_id,sport_id_user=int(message.text))
    bot.reply_to(message, 'успешно изменено!')
    main_menu_for_admin(message.chat.id)


def process_edit_schedule_step3_end(message):
    UserFlowAdmin().edit_schedule(id_outer=schedule_changed_id,t_end_user=message.text)
    bot.reply_to(message, 'успешно изменено!')
    main_menu_for_admin(message.chat.id)





def process_edit_schedule_step3_start(message):
    UserFlowAdmin().edit_schedule(id_outer=schedule_changed_id,t_start_user=message.text)
    bot.reply_to(message, 'успешно изменено!')
    main_menu_for_admin(message.chat.id)


@bot.message_handler(func=lambda message: message.text == "Удалить расписание" and Core().get_user(message.chat.id).is_admin())
def delete_schedule(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    item1 = types.KeyboardButton("Отмена")
    markup.add(item1)
    msg = bot.reply_to(message, 'введите id расписания', reply_markup=markup)
    bot.register_next_step_handler(msg, process_delete_schedule)
def process_delete_schedule(message):
    if message.text == 'Отмена':
        cancel_for_admin(message.chat.id)
        return
    else:
        try:
            if int(message.text):

                UserFlowAdmin().delete_schedule(message.text)
                bot.reply_to(message, 'успешно удалено!')
                main_menu_for_admin(message.chat.id)

            else:
                msg = bot.reply_to(message, 'введите корректный id расписания')
                bot.register_next_step_handler(msg, process_delete_schedule)
        except BaseException:
            bot.reply_to(message, 'Попробуйте еще раз')
            cancel_for_admin(message.chat.id)
            return
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(message.text)
    bot.reply_to(message, "Пожалуйста, используйте кнопки для взаимодействия.")
    core = Core()
    tg_user = message.from_user
    user = core.get_user(tg_user.id)
    if user.is_coach():
        main_menu_for_coach(message.chat.id)
    elif user.is_sportsman():
        main_menu_for_sportsman(message.chat.id)
    elif user.is_admin():
        main_menu_for_admin(message.chat.id)