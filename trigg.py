# -*- coding: utf-8 -*-

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import telebot
from telebot import types
import urllib3
import re
import requests
import time
from time import sleep
import datetime
from datetime import datetime
import _thread
import random
import tkn

# ======================================================================================================================
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds1 = ServiceAccountCredentials.from_json_keyfile_name('trigger1.json', scope)
client1 = gspread.authorize(creds1)
sheet1 = client1.open('Trigger').worksheet('main')
bot = telebot.TeleBot(tkn.tkn)

idMe = 396978030


def sprite():
    global g_trigger1
    global g_trigger2
    global g_trigger3
    global g_trigger4
    global g_trigger5
    global sheet1
    g_trigger1 = []
    g_trigger2 = []
    g_trigger3 = []
    g_trigger5 = []
    try:
        trigger_list1 = sheet1.col_values(1)
        RAW_g_trigger2 = sheet1.col_values(2)
        trigger_list3 = sheet1.col_values(3)
        g_trigger4 = sheet1.col_values(4)
        RAW_g_trigger5 = sheet1.col_values(5)
    except:
        creds1 = ServiceAccountCredentials.from_json_keyfile_name('trigger1.json', scope)
        client1 = gspread.authorize(creds1)
        sheet1 = client1.open('Trigger').worksheet('main')
        trigger_list1 = sheet1.col_values(1)
        RAW_g_trigger2 = sheet1.col_values(2)
        trigger_list3 = sheet1.col_values(3)
        g_trigger4 = sheet1.col_values(4)
        RAW_g_trigger5 = sheet1.col_values(5)
    trigger_list1.pop(0)
    RAW_g_trigger2.pop(0)
    trigger_list3.pop(0)
    g_trigger4.pop(0)
    RAW_g_trigger5.pop(0)
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
bot.send_message(idMe, '🤤')


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


@bot.message_handler(content_types=["new_chat_members"])
def get_new_member(message):
    if message.new_chat_member is not None:
        if message.new_chat_member.username == 'CWQ_bot':
            bot.send_message(message.chat.id, 'Жми /start')


@bot.message_handler(func=lambda message: message.text)
def repeat_all_messages(message):
    if message.text.lower().strip() in g_trigger1:
        try:
            text = g_trigger2[g_trigger1.index(message.text.lower().strip())]
        except:
            text = 'Я такого не знаю!'
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
    _thread.start_new_thread(google, ())
    telepol()
