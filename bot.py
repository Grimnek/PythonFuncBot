import telebot
from telebot import types

import time
import random
from string import digits, punctuation, ascii_letters
import uuid
import pafy
from gtts import gTTS
import os

import config

# Сюда подставляете свой токен
bot = telebot.TeleBot(config.TOKEN)

user_request = ''
user_result = None

#Приветствие при старте
@bot.message_handler(commands=['start'])
def welcome(message):

    # Клавиатура
    global markup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Убрать клавиатуру")
    item2 = types.KeyboardButton("Помощь")
    item3 = types.KeyboardButton("Загадать рандомное число")
    item4 = types.KeyboardButton("Сгенерировать сложный пароль")
    item5 = types.KeyboardButton("Сгенерировать рандомное ID")
    item6 = types.KeyboardButton("Скачать видео с ютуба")
    item7 = types.KeyboardButton("Конвертация текст в аудио")
    item8 = types.KeyboardButton("Youtube видео в аудио")

    markup.add(item1, item2).add(item3,item4,item5).add(item6, item7, item8)

    bot.send_message(message.chat.id, "Привет, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот с кучей функций. \n \n Если вам нужна информация обо мне,нажмите на клавишу Помощь.".format(message.from_user, bot.get_me()),
    parse_mode='html', reply_markup=markup)

#Открыть клавиатуру
@bot.message_handler(commands=['keyboard'])
def keyboard_on(message):
    global markup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Убрать клавиатуру")
    item2 = types.KeyboardButton("Помощь")
    item3 = types.KeyboardButton("Загадать рандомное число")
    item4 = types.KeyboardButton("Сгенерировать сложный пароль")
    item5 = types.KeyboardButton("Сгенерировать рандомное ID")
    item6 = types.KeyboardButton("Скачать видео с ютуба")
    item7 = types.KeyboardButton("Конвертация текст в аудио")
    item8 = types.KeyboardButton("Youtube видео в аудио")

    markup.add(item1, item2).add(item3, item4, item5).add(item6, item7, item8)
    bot.send_message(message.chat.id, 'Клавиатура включена', reply_markup=markup)

#Ответ на запрос клавиатуры
@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text == 'Загадать рандомное число':
        msg = bot.send_message(message.chat.id, 'Выберите число от 1 до 10')
        bot.register_next_step_handler(msg, randnum)
    elif message.text == 'Сгенерировать сложный пароль':
        symbols = digits + punctuation + ascii_letters
        sec_random = random.SystemRandom()
        hard_password = ''.join(sec_random.choice(symbols) for i in range (15))
        bot.send_message(message.chat.id, f'Ваш пароль:  {hard_password}')
    elif message.text == 'Убрать клавиатуру':
        bot.send_message(message.chat.id, 'Клавиатура убрана', reply_markup=types.ReplyKeyboardRemove())
    elif message.text == 'Помощь':
        bot.send_message(message.chat.id, f'###### Помощь ###### \n\n ### Убрать и вернуть клавиатуру ### \n /keyboard - Вернуть клавиатуру. \n Клавиша \'Убрать клавиатуру\' - Убрать клавиатуру. \n\n Помощь - гайд по боту. \n\n \'Загадать рандомное число\' - Игра на угадывания чисел от 1 до 10. \n\n \'Сгенерировать сложный пароль\' - Если у вас нет фантазии для создания пароля - вот ваш выбор! \n\n \'Сгенерировать рандомное ID\' - Нужно сгенерировать id? Тогда жмите на эту кнопку \n\n \'Скачать видео с ютуба\' - Качается видео с Youtube в высоком качестве. \n\n \'Конвертация текст в аудио\' - Вы пишете текст,мы его переделываем в аудио файл. \n\n \'Youtube видео в аудио\' - Если вам нужна песня,которая существует в качестве на Youtube,тогда вы можете этой командой извлечь из неё аудиозапись!')
    elif message.text == 'Сгенерировать рандомное ID':
        rand_id = uuid.uuid4()
        bot.send_message(message.chat.id, f'Ваш ID - {rand_id}')
    elif message.text == 'Скачать видео с ютуба':
        msg = bot.send_message(message.chat.id, 'Введите ссылку')
        bot.register_next_step_handler(msg, youtube_videos)
    elif message.text == 'Конвертация текст в аудио':
        msg = bot.send_message(message.chat.id, 'Что будем конвертировать?')
        bot.register_next_step_handler(msg, text_audio)
    elif message.text == 'Youtube видео в аудио':
        msg = bot.send_message(message.chat.id, 'Введите ссылку')
        bot.register_next_step_handler(msg, youtube_audio)
    else:
        pass

#Загадать рандомное число
def randnum(message, user_result = None):
    try:
        global user_request

        if user_result == None:
            user_request = int(message.text)
        else:
            user_request = str(user_result)
        bot.send_message(message.chat.id, 'Ну что-ж,давайте проверим.')
        NumberToGuess = random.randint(1, 10)
        time.sleep(2)
        if user_request == NumberToGuess:
            bot.send_message(message.chat.id, f'Поздравляю,вы угадали! Это действительно было число {NumberToGuess}')
        else:
            bot.send_message(message.chat.id, 'Не угадали.\n В другой раз вам точно повезет!')
    except Exception as e:
        bot.reply_to(message, 'Ошибка, попробуйте ещё раз!')

#Скачать видео с ютуба
def youtube_videos(message):
     bot.send_message(message.chat.id, 'Скачиваю видео...')
     try:
        global user_request

        if user_result == None:
            user_request = str(message.text)
        else:
            user_request = str(user_result)

        if "video.mp4" != None:
            os.remove('video.mp4')

        video = pafy.new(user_request)
        streams = video.streams
        best_stream = video.getbest()
        best_stream.download("video.mp4")
        bot.send_message(message.chat.id, 'Видео загружено! Пересылаю вам.')
        video_d = open("video.mp4", 'rb')
        bot.send_video(message.chat.id, video_d)
     except Exception as e:
         bot.reply_to(message, "Произошла ошибка! Проверьте свою ссылку ещё раз.")

#Конвертировать текст в аудио
def text_audio(message):
    bot.send_message(message.chat.id, 'Начинаю процесс конвертации.')
    try:
        global user_request

        if user_result == None:
            user_request = str(message.text)
        else:
            user_request = str(user_result)

        audio = 'audio.mp3'
        language = 'ru'
        sp = gTTS(text=user_request, lang=language, slow=False)
        sp.save(audio)
        bot.send_message(message.chat.id, 'Конвертация успешно завершена! Скидываю аудио.')
        audio_d = open("audio.mp3", 'rb')
        bot.send_audio(message.chat.id, audio_d)
    except Exception as e:
        bot.reply_to(message, "Что пошло не так... хм...")

#Youtube видео в аудио
def youtube_audio(message):
    bot.send_message(message.chat.id, 'Скачиваю видео...')
    try:
        global user_request

        if user_result == None:
            user_request = str(message.text)
        else:
            user_request = str(user_result)

        if "audio_youtube.mp3" != None:
            os.remove('audio_youtube.mp3')

        audio = pafy.new(user_request)
        audio_title = audio.title
        bot.send_message(message.chat.id, 'Провожу процесс конвертации.')
        best_audio = audio.getbestaudio()
        best_audio.download("audio_youtube.mp3")
        bot.send_message(message.chat.id, 'Готово! Скидываю аудиозапись с названием.')
        audio_d = open("audio_youtube.mp3", 'rb')
        bot.send_message(message.chat.id, audio_title)
        bot.send_audio(message.chat.id, audio_d)
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка! Проверьте свою ссылку ещё раз.")

# RUN
bot.polling(none_stop=True)