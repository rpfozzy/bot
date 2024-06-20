import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
import requests

# Вставьте ваш токен сюда
token = '6884297621:AAGduHkNhhs08N--1B1rsh4rsMycmjocuXo'

# Создайте экземпляр TeleBot
bot = telebot.TeleBot(token)

# Код доступа для скачивания видео
ACCESS_CODE = '2007'
user_state = {}

# Функция для обработки команды /start
@bot.message_handler(commands=['start'])
def start(message):
    text = """
*Здравствуйте\\!*
*Связь с админом, предложения автору ресурс паков и помощь доступны в этом боте\\!*
*Как мы можем помочь вам сейчас\\?*
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    web_app_button = KeyboardButton("RPFOZZY WEBSITE", web_app=WebAppInfo(url="https://rpfozzy.github.io/index/#"))
    keyboard.add(web_app_button)
    
    bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode='MarkdownV2')

# Функция для обработки команды /y
@bot.message_handler(commands=['y'])
def request_code(message):
    bot.send_message(message.chat.id, "Введите код:")
    user_state[message.chat.id] = 'WAITING_FOR_CODE'

# Функция для обработки текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.chat.id in user_state:
        state = user_state[message.chat.id]
        if state == 'WAITING_FOR_CODE':
            if message.text == ACCESS_CODE:
                bot.send_message(message.chat.id, "Код принят! Введите ссылку на видео с YouTube:")
                user_state[message.chat.id] = 'WAITING_FOR_LINK'
            else:
                bot.send_message(message.chat.id, "Неверный код. Попробуйте снова.")
        elif state == 'WAITING_FOR_LINK':
            link = message.text
            try:
                yt = YouTube(link)
                video_title = yt.title
                duration = yt.length
