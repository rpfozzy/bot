import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# Вставьте ваш токен сюда
token = '6884297621:AAGduHkNhhs08N--1B1rsh4rsMycmjocuXo'
admin_id = 1653222949

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
    ad_button = KeyboardButton("РЕКЛАМА НА КАНАЛЕ @RPFOZZY")
    keyboard.add(web_app_button, ad_button)
    
    bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode='MarkdownV2')

# Функция для обработки нажатий на кнопку "РЕКЛАМА НА КАНАЛЕ @RPFOZZY"
@bot.message_handler(func=lambda message: message.text == "РЕКЛАМА НА КАНАЛЕ @RPFOZZY")
def send_ad_info(message):
    discount_text = """
*АКЦИЯ \\-20\\% НА РЕКЛАМУ ДО 1 АВГУСТА:*

*Неделя:*
ГРН — 48 гривен 
\\[850 просмотров\\]
РУБ — 102 рубля

*2 недели:*
ГРН — от 80 грн \\| до 160 грн
\\[2000 просмотров\\]
РУБ — от 175 руб \\| до 352 руб

*3 недели:*
ГРН — от 120 грн \\| до 240 грн
\\[2700 просмотров\\]
РУБ — от 260 руб \\| до 528 руб

*4 недели \\(месяц\\):*
ГРН — от 160 грн \\| до 320 грн
\\[3000 просмотров\\]
РУБ — от 352 руб \\| до 700 руб

*Дополнительные варианты:*

*Навсегда:*
ГРН — 444 гривен
РУБ — 976 рублей
\\[Просмотры зависят от разных факторов, обычно старые посты набирают 8000\\-10000 просмотров\\]
    """
    
    try:
        bot.send_message(message.chat.id, discount_text, parse_mode='MarkdownV2')
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

# Функция для пересылки сообщений админу и добавления кнопки для ответа
@bot.message_handler(func=lambda message: True)
def forward_message_to_admin(message):
    if message.chat.id != admin_id:
        bot.forward_message(admin_id, message.chat.id, message.message_id)
        
        markup = InlineKeyboardMarkup()
        reply_button = InlineKeyboardButton("Ответить на сообщение", callback_data=f"reply_{message.chat.id}")
        markup.add(reply_button)
        
        bot.send_message(admin_id, "Вы получили новое сообщение. Вы можете ответить на него.", reply_markup=markup)

# Функция для обработки нажатий на кнопку "Ответить на сообщение"
@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def ask_for_reply(call):
    chat_id = call.data.split("_")[1]
    bot.send_message(admin_id, f"Напишите сообщение, и я отправлю его пользователю. ID пользователя: {chat_id}")
    bot.register_next_step_handler_by_chat_id(admin_id, send_reply, chat_id)

# Функция для отправки ответа пользователю
def send_reply(message, chat_id):
    try:
        bot.send_message(chat_id, message.text)
        bot.send_message(admin_id, "Сообщение отправлено.")
    except Exception as e:
        bot.send_message(admin_id, f"Ошибка: {e}")

# Запуск бота
bot.polling(none_stop=True)