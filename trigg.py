# -*- coding: utf-8 -*-

import os
import gspread
import telebot
from time import sleep
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials


def environmental_files():
    directory = os.listdir('.')
    for key in os.environ.keys():
        if key.endswith('.json') and key not in directory:
            file = open(key, 'w')
            file.write(os.environ.get(key))
            file.close()


environmental_files()
# ======================================================================================================================
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds1 = ServiceAccountCredentials.from_json_keyfile_name('trigger1.json', scope)
client1 = gspread.authorize(creds1)
sheet1 = client1.open('Trigger').worksheet('main')
bot = telebot.TeleBot(os.environ['TOKEN'])

idMe = 396978030
idCh = -1001153670526


def logdata(message):
    stamp = int(datetime.now().timestamp())
    weekday = datetime.utcfromtimestamp(int(stamp + 3 * 60 * 60)).strftime('%a')
    if weekday == 'Mon':
        weekday = 'Пн'
    elif weekday == 'Tue':
        weekday = 'Вт'
    elif weekday == 'Wed':
        weekday = 'Ср'
    elif weekday == 'Thu':
        weekday = 'Чт'
    elif weekday == 'Fri':
        weekday = 'Пт'
    elif weekday == 'Sat':
        weekday = 'Сб'
    elif weekday == 'Sun':
        weekday = 'Вс'
    day = datetime.utcfromtimestamp(int(stamp + 3 * 60 * 60)).strftime('%d')
    month = datetime.utcfromtimestamp(int(stamp + 3 * 60 * 60)).strftime('%m')
    year = datetime.utcfromtimestamp(int(stamp + 3 * 60 * 60)).strftime('%Y')
    hours = datetime.utcfromtimestamp(int(stamp + 3 * 60 * 60)).strftime('%H')
    minutes = datetime.utcfromtimestamp(int(stamp)).strftime('%M')
    seconds = datetime.utcfromtimestamp(int(stamp)).strftime('%S')
    data = '\n<code>' + str(weekday) + ' ' + str(day) + '.' + str(month) + '.' + str(year) + \
           ' ' + str(hours) + ':' + str(minutes) + ':' + str(seconds) + '</code> '
    if message != 0:
        try:
            kind = message.chat
            if message.chat.id < 0:
                kind = message.from_user
        except:
            kind = message.from_user
        firstname = ''
        lastname = ''
        username = 'None'
        if kind.first_name:
            firstname = str(kind.first_name) + ' '
        if kind.last_name:
            lastname = str(kind.last_name) + ' '
        if kind.username:
            username = str(kind.username)
        data = data + firstname + lastname + '[@' + username + '] <code>' + \
            str(kind.id) + '</code>:\n<code>&#62;&#62;</code> '
    return data


def sprite():
    global g_trigger1
    global g_trigger2
    global g_trigger3
    global g_trigger4
    global g_trigger5
    global bit1
    global bit2

    global sheet1
    g_trigger1 = []
    g_trigger2 = []
    g_trigger3 = []
    g_trigger5 = []
    bit1 = []
    bit2 = []
    try:
        trigger_list1 = sheet1.col_values(2)
        RAW_g_trigger2 = sheet1.col_values(3)
        trigger_list3 = sheet1.col_values(5)
        g_trigger4 = sheet1.col_values(6)
        RAW_g_trigger5 = sheet1.col_values(7)
        bit1 = sheet1.col_values(1)
        bit2 = sheet1.col_values(4)

    except:
        creds1 = ServiceAccountCredentials.from_json_keyfile_name('trigger1.json', scope)
        client1 = gspread.authorize(creds1)
        sheet1 = client1.open('Trigger').worksheet('main')
        trigger_list1 = sheet1.col_values(2)
        RAW_g_trigger2 = sheet1.col_values(3)
        trigger_list3 = sheet1.col_values(5)
        g_trigger4 = sheet1.col_values(6)
        RAW_g_trigger5 = sheet1.col_values(7)
        bit1 = sheet1.col_values(1)
        bit2 = sheet1.col_values(4)

    trigger_list1.pop(0)
    RAW_g_trigger2.pop(0)
    trigger_list3.pop(0)
    g_trigger4.pop(0)
    RAW_g_trigger5.pop(0)
    bit1.pop(0)
    bit2.pop(0)
    for t1 in trigger_list1:
        g_trigger1.append(t1.lower().strip())
    for t3 in trigger_list3:
        g_trigger3.append(t3.lower().strip())
    for t2 in RAW_g_trigger2:
        if len(t2) > 4000:
            t2 = t2[:4000]
        g_trigger2.append(t2)
    for t5 in RAW_g_trigger5:
        if len(t5) > 4000:
            t5 = t5[:4000]
        g_trigger5.append(t5)
# ======================================================================================================================


sprite()


@bot.message_handler(commands=['id'])
def handle_id_command(message):
    if message.chat.id > 0:
        bot.send_message(message.chat.id, "Твой ID: " + str(message.chat.id))
    elif message.chat.id < 0:
        bot.send_message(message.chat.id, "ID этой группы: " + str(message.chat.id))


@bot.message_handler(commands=['update'])
def handle_id_command(message):
    if message.chat.id == idMe or message.chat.id == 343663939:
        sprite()
        bot.send_message(message.chat.id, 'Обновлено')


@bot.message_handler(content_types=['photo'])
def redmessages(message):
    if message.chat.id == idMe or message.chat.id == 343663939:
        if message.photo:
            bot.send_message(message.chat.id, 'file_id: ' + str(message.photo[0].file_id))


@bot.message_handler(func=lambda message: message.text)
def repeat_all_messages(message):
    if message.text.lower().strip() in g_trigger1:
        try:
            text = g_trigger2[g_trigger1.index(message.text.lower().strip())]
        except:
            text = 'Я такого не знаю!'
        try:
            bits = bit1[g_trigger1.index(message.text.lower().strip())]
        except:
            bits = ''
        if bits != '':
            bot.send_message(idCh, logdata(message) + bits, parse_mode='HTML')

        bot.send_message(message.chat.id, text)
    elif message.text.lower().strip() in g_trigger3:
        try:
            fileid = g_trigger4[g_trigger3.index(message.text.lower().strip())]
            if g_trigger5[g_trigger3.index(message.text.lower().strip())] == '':
                caption = None
            else:
                try:
                    caption = g_trigger5[g_trigger3.index(message.text.lower().strip())]
                except:
                    caption = None
            try:
                bits = bit2[g_trigger3.index(message.text.lower().strip())]
            except:
                bits = ''
            if bits != '':
                bot.send_message(idCh, logdata(message) + bits, parse_mode='HTML')

            bot.send_photo(message.chat.id, fileid, caption)
        except:
            text = 'Я такого не знаю~!'
            bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, 'Я такого не знаю')


def telepol():
    try:
        bot.polling(none_stop=True, timeout=60)
    except:
        bot.stop_polling()
        sleep(0.5)
        telepol()


if __name__ == '__main__':
    telepol()
