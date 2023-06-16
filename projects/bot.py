import telebot
from telebot import types

import os

import requests

from datetime import datetime, timedelta


token = '5966090902:AAFJjESoK1ttHrhsMeNCWS_irf_gY9r-1E4'


URL = 'http://127.0.0.1:8000/api/projects/'
MAIN_URL = 'http://127.0.0.1:8000/api/userappeal/'

bot = telebot.TeleBot(token)


start_keyboard = types.ReplyKeyboardMarkup(True)
create_btn = 'СОЗДАТЬ'
get_projects = 'СПИСОК ПРОЕКТОВ'
get_appeal = 'ЗАЯВКИ'
start_keyboard.add(create_btn, get_projects, get_appeal)


update_keyboard = types.ReplyKeyboardMarkup(True)
title = 'НАЗВАНИЕ'
description = 'ОПИСАНИЕ'
photo = 'ФОТО'


update_keyboard.add(title, description, photo)
delete_data = 'УДАЛИТЬ'
update_data = 'ИЗМЕНИТЬ'


@bot.message_handler(func=lambda message: message.text == get_appeal)
def handle_appeal_button(message):
    appeal_keyboard = types.ReplyKeyboardMarkup(True)
    appeal_week = 'ЗАЯВКИ ЗА НЕДЕЛЮ'
    appeal_month = 'ЗАЯВКИ ЗА МЕСЯЦ'
    appeal_year = 'ЗАЯВКИ ЗА ГОД'
    appeal_keyboard.add(appeal_week, appeal_month, appeal_year)
    bot.send_message(message.chat.id, 'ВЫБЕРИТЕ ПЕРИОД ЗАЯВОК:', reply_markup=appeal_keyboard)


@bot.message_handler(func=lambda message: message.text == 'ЗАЯВКИ ЗА НЕДЕЛЮ')
def handle_appeal_week_button(message):
    result = requests.get(f'{MAIN_URL}get_week/').json()
    for i in result:
        bot.send_message(message.chat.id, f'{i["name"]}\n\n{i["mail"]}\n\n{i["message"]}\n\n{i["date"]}')


@bot.message_handler(func=lambda message: message.text == 'ЗАЯВКИ ЗА МЕСЯЦ')
def handle_appeal_month_button(message):
    result = requests.get(f'{MAIN_URL}get_month/').json()
    for i in result:
        bot.send_message(message.chat.id, f'{i["name"]}\n\n{i["mail"]}\n\n{i["message"]}\n\n{i["date"]}')


@bot.message_handler(func=lambda message: message.text == 'ЗАЯВКИ ЗА ГОД')
def handle_appeal_year_button(message):
    result = requests.get(f'{MAIN_URL}get_year/').json()
    for i in result:
        bot.send_message(message.chat.id, f'{i["name"]}\n\n{i["mail"]}\n\n{i["message"]}\n\n{i["date"]}')


def del_upd_keyb(id):
    delete = types.InlineKeyboardButton('УДАЛИТЬ', callback_data=f'УДАЛИТЬ {id}')
    update = types.InlineKeyboardButton('ИЗМЕНИТЬ', callback_data=f'ИЗМЕНИТЬ {id}')
    del_upd_keyboard = types.InlineKeyboardMarkup()
    del_upd_keyboard.add(delete, update)
    return del_upd_keyboard


datas = {}
update_datas = {}


def create_dir():
    dir = os.path.join("media")
    if not os.path.exists(dir):
        os.mkdir(dir)


@bot.message_handler(commands=["start"])
def send_mess(message):
    bot.send_message(
        message.chat.id, 'ПРИВЕТ!!!',
        reply_markup=start_keyboard,
    )

def get_name(message):
    datas['name'] = message.text
    msg = bot.send_message(message.chat.id, 'ВВЕДИТЕ ОПИСАНИЕ')
    bot.register_next_step_handler(msg, get_description)


def get_description(message):
    description = message.text
    datas['description'] = description
    msg = bot.send_message(message.chat.id, 'ЗАГРУЗИТЕ ФОТО ПРОЕКТА')
    bot.register_next_step_handler(msg, get_documents)


def get_documents(message):
    file_name = message.photo[-1].file_id
    file_id_info = bot.get_file(file_name)
    downloaded_file = bot.download_file(file_id_info.file_path)
    create_dir()
    image_path = f'./media/document_{datetime.now().strftime("%Y%m%d%H%M%S")}.jpeg'
    datas['photo'] = image_path
    with open(image_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(message.chat.id, 'УСПЕШНО СОХРАНЕНО')
    files = {'photo': open(datas.pop('photo'), 'rb')}
    response = requests.post(URL, datas, files=files)
    print(response.status_code)
    datas.clear()
    os.remove(image_path)


def update_project(project_id, data, message):
    response = requests.patch(f'{URL}{project_id}/', data)
    sc = response.status_code
    if sc == 404:
        bot.send_message(message.chat.id, 'ПРОЕКТ С ТАКИМ id НЕ СУЩЕСТВУЕТ')
    else:
        bot.send_message(message.chat.id, f'ПРОЕКТ С id {project_id} УСПЕШНО ИЗМЕНЕН')


def update_progect_image(project_id, files, message):
    response = requests.patch(f'{URL}{project_id}/', {}, files=files)
    sc = response.status_code
    if sc == 404:
        bot.send_message(message.chat.id, 'ПРОЕКТА С ТАКИМ id НЕ СУЩЕСТВУЕТ')
    else:
        bot.send_message(message.chat.id, f'ПРОЕКТ С  id {project_id} УСПЕШНО ИЗМЕНЕН')


def update_name(message):
    update_datas['name'] = message.text
    update_project(update_datas.pop('id'), update_datas, message)
    update_datas.clear()
    bot.send_message(message.chat.id, 'НАЗВАНИЕ ИЗМЕНЕНО', reply_markup=start_keyboard)


def update_description(message):
    update_datas['description'] = message.text
    update_project(update_datas.pop('id'), update_datas, message)
    update_datas.clear()
    bot.send_message(message.chat.id, 'ОПИСАНИЕ ИЗМЕНЕНО', reply_markup=start_keyboard)


def update_photo(message):
    file_name = message.photo[-1].file_id
    file_id_info = bot.get_file(file_name)
    downloaded_file = bot.download_file(file_id_info.file_path)
    create_dir()
    image_path = f'./media/document_{datetime.now().strftime("%Y%m%d%H%M%S")}.jpeg'
    update_datas['photo'] = image_path
    with open(image_path, 'wb') as new_file:
        new_file.write(downloaded_file)   
    files = {'photo': open(update_datas.pop('photo'), 'rb')}
    update_progect_image(update_datas.pop('id'), files, message)
    update_datas.clear()
    os.remove(image_path)
    bot.send_message(message.chat.id, 'ФОТО ИЗМЕНЕНО', reply_markup=start_keyboard)


def get_proj():
    return requests.get(URL).json()


@bot.message_handler(content_types=["text"])
def get_messages(message):
    if message.text == create_btn:
        msg = bot.send_message(message.chat.id, 'ВВЕДИТЕ НАЗВАНИЕ ПРОЕКТА')
        bot.register_next_step_handler(msg, get_name)
    elif message.text == get_projects:
        json_proj = get_proj()
        if json_proj == []:
            bot.send_message(message.chat.id, 'В БАЗЕ ДАННЫХ НЕТ ПРОЕКТОВ')
        else:
            for p in json_proj:
                mesg = f"{p['name']}"
                bot.send_message(message.chat.id, mesg, reply_markup=del_upd_keyb(p.get('id')))
    elif message.text == title:
        msg = bot.send_message(message.chat.id, 'ВВЕДИТЕ НОВОЕ НАЗВАНИЕ ПРОЕКТА')
        bot.register_next_step_handler(msg, update_name)
    elif message.text == description:
        msg = bot.send_message(message.chat.id, 'ВВЕДИТЕ НОВОЕ ОПИСАНИЕ ПРОЕКТА')
        bot.register_next_step_handler(msg, update_description)
    elif message.text == photo:# image
        msg = bot.send_message(message.chat.id, 'ПРИШЛИТЕ НОВУЮ КАРТИНКУ ПРОЕКТА')
        bot.register_next_step_handler(msg, update_photo)#update


def delete_project(project_id, message):
    response = requests.delete(f'{URL}{project_id}/')
    sc = response.status_code
    if sc == 404:
        bot.send_message(message.chat.id, 'ПРОЕКТА С id НЕ СУЩЕСТВУЕТ')
    else:
        bot.send_message(message.chat.id, f'ПРОЕКТ С  id {project_id} УСПЕШНО УДАЛЕН')


@bot.callback_query_handler(func=lambda call: True)
def appel_query(call):
    if delete_data in call.data:
        ids = call.data.split(' ')[1]
        delete_project(ids, call.message)
    elif update_data in call.data:
        update_datas['id'] = call.data.split(' ')[1]
        bot.send_message(call.message.chat.id, 'КАКОЕ ПОЛЕ ВЫ ХОТИТЕ ИЗМЕНИТЬ?', reply_markup=update_keyboard)


if __name__ == "__main__":
    bot.polling(none_stop=True)