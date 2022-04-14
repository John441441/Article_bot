import telebot
import requests
from telebot import types
import json

bot = telebot.TeleBot('5189743525:AAE84_3h90523vSDqDUISMr73kBMwrSvTaM')



@bot.message_handler(commands = ['Start', 'СТАРТ'])
def open_message(message):
    """Сообщение для активации поиска по артикулу"""
    bot.send_message(message.chat.id, 'Введите номер артикула:', parse_mode='html')
    global article
    article = message.text


@bot.message_handler(content_types=['text'])
def open_message2(message):
    """Проверка количества символов в артикуле. Если False, то просит ввести корректные данные"""
    if len(message.text) == 8:
        msg = bot.send_message(message.chat.id, 'Введите новое название этого артикула, не более 100 символов:', parse_mode='html')
        bot.register_next_step_handler(msg, open_message3)

    else:
        msg = bot.send_message(message.chat.id, 'Артикул состоит из 8 символов, введите снова:', parse_mode='html')
        bot.register_next_step_handler(msg, open_message2)



@bot.message_handler(content_types=['text'])
def open_message3(message):
    if len(message.text) > 100:
        name = message.text[0:100]
        # На текущий момент нет актуального API от "Wildberries"
        # req = requests.get(
        #     "https://suppliers-stats.wildberries.ru/api/v1/supplier/stocks?dateFrom=2017-03-25T21:00:00.000Z&key=NTQwOTQzNTMtMDUwNC00MWMyLWEzMDktNzI4NTY1MGE5OTI2")
        # data = json.loads(req.text)
        #
        # for i in data:
        #     if i['subject'] == article:
        #         i['subject'] = name
        #
        # with open('name_subject.json', 'w', encoding='utf-8') as file:
        #     json.dump(data, file, indent=4)
    keyboard = types.ReplyKeyboardMarkup()
    key_response = types.InlineKeyboardButton(text = 'Да', resizeKeyboard=True)
    keyboard.add(key_response)
    key_response2 = types.InlineKeyboardButton(text = 'Нет', resizeKeyboard=True, callback_data = 'replay')
    keyboard.add(key_response2)
    msg = bot.send_message(message.from_user.id, text = 'Название товара изменено?', reply_markup=keyboard)

    """Запрос с сервера Wildberries о наличии данного артикула и замене наименования товара"""

@bot.callback_query_handler(func = lambda call: True)
def callback_worker(call, message):
    "Вызов функции, которая возвращает в начало, если изменение названия не произошло"
    msg = bot.send_message(message.chat.id, 'Попробуйте снова!:', parse_mode='html')
    if call.data == 'replay':
        bot.register_next_step_handler(msg, open_message2)


bot.infinity_polling()

