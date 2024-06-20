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
                thumbnail_url = yt.thumbnail_url
                
                # Генерация кнопок для скачивания
                keyboard = InlineKeyboardMarkup()
                for stream in yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution'):
                    res = stream.resolution
                    size = round(stream.filesize / (1024 * 1024), 2)  # размер файла в МБ
                    button_text = f'{res} MP4 ({size} MB)'
                    callback_data = f'download|{stream.itag}'
                    keyboard.add(InlineKeyboardButton(button_text, callback_data=callback_data))

                # Добавление кнопок для видео 720p и 1080p, если они не прогрессивные
                for stream in yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution'):
                    res = stream.resolution
                    if res in ['720p', '1080p']:
                        size = round(stream.filesize / (1024 * 1024), 2)  # размер файла в МБ
                        button_text = f'{res} MP4 ({size} MB)'
                        callback_data = f'download|{stream.itag}'
                        keyboard.add(InlineKeyboardButton(button_text, callback_data=callback_data))

                # Добавление аудио кнопок
                audio_stream = yt.streams.filter(only_audio=True).first()
                audio_size = round(audio_stream.filesize / (1024 * 1024), 2)  # размер файла в МБ
                keyboard.add(InlineKeyboardButton(f'320kbps .mp3 ({audio_size} MB)', callback_data=f'download_audio|{audio_stream.itag}'))

                bot.send_message(message.chat.id, f"Видео: {video_title}\nПродолжительность: {duration} сек", reply_markup=keyboard)
                user_state[message.chat.id] = {
                    'state': 'AWAITING_DOWNLOAD',
                    'link': link,
                    'title': video_title,
                    'duration': duration,
                    'thumbnail_url': thumbnail_url
                }
            except Exception as e:
                bot.send_message(message.chat.id, f"Ошибка при обработке видео. Проверьте ссылку и попробуйте снова.\nОшибка: {str(e)}")
                user_state.pop(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Введите команду /y для начала процесса скачивания видео с YouTube.")

# Функция для обработки нажатий на кнопки
@bot.callback_query_handler(func=lambda call: call.data.startswith('download|'))
def handle_download(call):
    try:
        chat_id = call.message.chat.id
        if chat_id not in user_state or 'link' not in user_state[chat_id]:
            bot.send_message(chat_id, "Ошибка состояния. Попробуйте снова.")
            return

        itag = call.data.split('|')[1]
        link = user_state[chat_id]['link']
        video_title = user_state[chat_id]['title']
        duration = user_state[chat_id]['duration']
        thumbnail_url = user_state[chat_id]['thumbnail_url']
        
        yt = YouTube(link)
        stream = yt.streams.get_by_itag(itag)
        filename = stream.default_filename
        stream.download(filename=filename)

        # Скачиваем миниатюру
        thumbnail_path = 'thumbnail.jpg'
        with open(thumbnail_path, 'wb') as thumb_file:
            thumb_file.write(requests.get(thumbnail_url).content)

        with open(filename, 'rb') as file:
            bot.send_video(chat_id, file, thumb=open(thumbnail_path, 'rb'), caption=f"{video_title}\nПродолжительность: {duration} сек")

        bot.send_message(chat_id, f"Скачивание завершено. Видео сохранено как {filename}.")
        os.remove(filename)
        os.remove(thumbnail_path)
        user_state.pop(chat_id)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Ошибка при скачивании видео. Попробуйте снова.\nОшибка: {str(e)}")

# Функция для обработки нажатий на кнопки для аудио
@bot.callback_query_handler(func=lambda call: call.data.startswith('download_audio|'))
def handle_download_audio(call):
    try:
        chat_id = call.message.chat.id
        if chat_id not in user_state or 'link' not in user_state[chat_id]:
            bot.send_message(chat_id, "Ошибка состояния. Попробуйте снова.")
            return

        itag = call.data.split('|')[1]
        link = user_state[chat_id]['link']
        video_title = user_state[chat_id]['title']
        duration = user_state[chat_id]['duration']
        
        yt = YouTube(link)
        stream = yt.streams.get_by_itag(itag)
        filename = stream.default_filename
        stream.download(filename=filename)
        
        # Конвертация в mp3
        audio = AudioFileClip(filename)
        audio_filename = filename.replace('.mp4', '.mp3')
        audio.write_audiofile(audio_filename, codec='libmp3lame', bitrate='320k')

        with open(audio_filename, 'rb') as audio_file:
            bot.send_audio(chat_id, audio_file, caption=f"{video_title}\nПродолжительность: {duration} сек")

        bot.send_message(chat_id, f"Скачивание завершено. Аудио сохранено как {audio_filename}.")
        os.remove(filename)
        os.remove(audio_filename)
        user_state.pop(chat_id)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Ошибка при скачивании аудио. Попробуйте снова.\nОшибка: {str(e)}")

# Запуск бота
bot.polling()