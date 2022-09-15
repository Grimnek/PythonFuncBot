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

bot = telebot.TeleBot(config.TOKEN)

user_request = ''
user_result = None


@bot.message_handler(commands=['start'])
def welcome(message):
    # Клавиатура
    global markup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Прибрати клавіатуру")
    item2 = types.KeyboardButton("Допомога")
    item3 = types.KeyboardButton("Загадати рандомне число")
    item4 = types.KeyboardButton("Згенерувати складний пароль")
    item5 = types.KeyboardButton("Згенерувати рандомне ID")
    item6 = types.KeyboardButton("Завантажити відео з ютуба")
    item7 = types.KeyboardButton("Конвертація тексту в аудіо")
    item8 = types.KeyboardButton("Youtube відео в аудіо")

    markup.add(item1, item2).add(item3, item4, item5).add(item6, item7, item8)

    bot.send_message(message.chat.id,
                     "Вітання, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот з купою функцій. \n \n Якщо вам потрібна інформація про мене, натисніть клавішу Допомога.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['keyboard'])
def keyboard_on(message):
    global markup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Прибрати клавіатуру")
    item2 = types.KeyboardButton("Допомога")
    item3 = types.KeyboardButton("Загадати рандомне число")
    item4 = types.KeyboardButton("Згенерувати складний пароль")
    item5 = types.KeyboardButton("Згенерувати рандомне ID")
    item6 = types.KeyboardButton("Завантажити відео з ютуба")
    item7 = types.KeyboardButton("Конвертація тексту в аудіо")
    item8 = types.KeyboardButton("Youtube відео в аудіо")

    markup.add(item1, item2).add(item3, item4, item5).add(item6, item7, item8)
    bot.send_message(message.chat.id, 'Клавіатура увімкнена', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text == 'Загадати рандомне число':
        msg = bot.send_message(message.chat.id, 'Виберіть число від 1 до 10')
        bot.register_next_step_handler(msg, randnum)
    elif message.text == 'Згенерувати складний пароль':
        symbols = digits + punctuation + ascii_letters
        sec_random = random.SystemRandom()
        hard_password = ''.join(sec_random.choice(symbols) for i in range(15))
        bot.send_message(message.chat.id, f'Ваш пароль:  {hard_password}')
    elif message.text == 'Прибрати клавіатуру':
        bot.send_message(message.chat.id, 'Клавіатура прибрана', reply_markup=types.ReplyKeyboardRemove())
    elif message.text == 'Допомога':
        bot.send_message(message.chat.id,
                         f'###### Допомога ###### \n\n ### Прибрати та повернути клавіатуру ### \n /keyboard - Повернути клавіатуру. \n Кнопка \'Прибрати клавіатуру\' - Прибрати клавіатуру. \n\n Допомога - гайд по боту. \n\n \'Загадати рандомне число\' - Гра на вгадування чисел від 1 до 10. \n\n \'Згенерувати складний пароль\' - Якщо у вас немає фантазії для створення пароля – ось ваш вибір \n\n \'Згенерувати рандомне ID\' - Потрібно згенерувати ID? Тоді натисніть на цю кнопку \n\n \'Завантажити відео з ютуба\' - Качається відео з Youtube у високій якості. \n\n \'Конвертація тексту в аудіо\' - Ви пишете текст, ми його переробляємо в аудіо файл. \n\n \'Youtube відео в аудіо\' - Якщо вам потрібна пісня, яка існує як Youtube, тоді ви можете цією командою витягти з неї аудіозапис!')
    elif message.text == 'Згенерувати рандомне ID':
        rand_id = uuid.uuid4()
        bot.send_message(message.chat.id, f'Ваш ID - {rand_id}')
    elif message.text == 'Завантажити відео з ютуба':
        msg = bot.send_message(message.chat.id, 'Введіть посилання')
        bot.register_next_step_handler(msg, youtube_videos)
    elif message.text == 'Конвертація тексту в аудіо':
        msg = bot.send_message(message.chat.id, 'Що конвертуватимемо?')
        bot.register_next_step_handler(msg, text_audio)
    elif message.text == 'Youtube відео в аудіо':
        msg = bot.send_message(message.chat.id, 'Введіть посилання')
        bot.register_next_step_handler(msg, youtube_audio)
    else:
        pass


def randnum(message, user_result=None):
    try:
        global user_request

        if user_result == None:
            user_request = int(message.text)
        else:
            user_request = str(user_result)
        bot.send_message(message.chat.id, 'Ну що ж, давайте перевіримо.')
        NumberToGuess = random.randint(1, 10)
        time.sleep(2)
        if user_request == NumberToGuess:
            bot.send_message(message.chat.id, f'Вітаю, ви вгадали! Це справді було число {NumberToGuess}')
        else:
            bot.send_message(message.chat.id, 'Не вгадали.\n Інший раз вам точно пощастить!')
    except Exception as e:
        bot.reply_to(message, 'Помилка, спробуйте ще раз')


def youtube_videos(message):
    bot.send_message(message.chat.id, 'Завантажую відео...')
    try:
        global user_request

        if user_result == None:
            user_request = str(message.text)
        else:
            user_request = str(user_result)

        if "video.mp4" != None:
            os.remove('video.mp4')

        video = pafy.new(user_request)
        best_stream = video.getbest()
        best_stream.download("video.mp4")
        bot.send_message(message.chat.id, 'Відео завантажено! Пересилаю вам.')
        video_d = open("video.mp4", 'rb')
        bot.send_video(message.chat.id, video_d)
    except Exception as e:
        bot.reply_to(message, "Виникла помилка! Перевірте посилання ще раз.")


def text_audio(message):
    bot.send_message(message.chat.id, 'Починаю процес конвертації.')
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
        bot.send_message(message.chat.id, 'Конвертацію успішно завершено! Скидаю аудіо.')
        audio_d = open("audio.mp3", 'rb')
        bot.send_audio(message.chat.id, audio_d)
    except Exception as e:
        bot.reply_to(message, "Щось пішло не так...")



def youtube_audio(message):
    bot.send_message(message.chat.id, 'Завантажую відео...')
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
        bot.send_message(message.chat.id, 'Починаю процес конвертації.')
        best_audio = audio.getbestaudio()
        best_audio.download("audio_youtube.mp3")
        bot.send_message(message.chat.id, 'Готово! Знижую аудіозапис з назвою.')
        audio_d = open("audio_youtube.mp3", 'rb')
        bot.send_message(message.chat.id, audio_title)
        bot.send_audio(message.chat.id, audio_d)
    except Exception as e:
        bot.reply_to(message, "Виникла помилка! Перевірте посилання ще раз.")



bot.polling(none_stop=True)
