import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Вставьте ваш токен сюда
token = '6884297621:AAGduHkNhhs08N--1B1rsh4rsMycmjocuXo'

# Создайте экземпляр TeleBot
bot = telebot.TeleBot(token)

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

# Запуск бота
bot.polling()
