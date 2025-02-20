import telebot
from telebot import types
import time
import random
from string import digits, punctuation, ascii_letters
import uuid
from gtts import gTTS
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
user_request = ''
user_result = None


@bot.message_handler(commands=['start'])
def welcome(message):
    global markup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Remove keyboard")
    item2 = types.KeyboardButton("Help")
    item3 = types.KeyboardButton("Generate a random number")
    item4 = types.KeyboardButton("Generate a complex password")
    item5 = types.KeyboardButton("Generate a random ID")
    item6 = types.KeyboardButton("Convert text to audio")

    markup.add(item1, item2, item3).add(item4, item5, item6)

    bot.send_message(message.chat.id,
                     "Hi, {0.first_name}!"
                     "\nI am <b>{1.first_name}</b>, a bot with many functions."
                     "\n \n If you need information about me, press the Help button.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['keyboard'])
def keyboard_on(message):
    global markup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Remove keyboard")
    item2 = types.KeyboardButton("Help")
    item3 = types.KeyboardButton("Generate a random number")
    item4 = types.KeyboardButton("Generate a complex password")
    item5 = types.KeyboardButton("Generate a random ID")
    item6 = types.KeyboardButton("Convert text to audio")

    markup.add(item1, item2, item3).add(item4, item5, item6)
    bot.send_message(message.chat.id, 'The keyboard is enabled', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text == 'Remove keyboard':
        bot.send_message(message.chat.id, 'The keyboard is removed', reply_markup=types.ReplyKeyboardRemove())
    elif message.text == 'Help':
        bot.send_message(message.chat.id,
                         f'###### Help ###### '
                         f'\n\n /keyboard - Remove the keyboard. '
                         f'\n\n Button "Remove Keyboard" - Remove the keyboard. '
                         f'\n\n Help - Guide to the bot. '
                         f'\n\n "Generate a random number" - A number guessing game from 1 to 10. '
                         f'\n\n "Generate a complex password" - '
                         f'If you have no imagination for creating a password – this is your choice. '
                         f'\n\n "Generate a random ID" - Need to generate an ID? Then press this button. '
                         f'\n\n "Convert text to audio" - You write text, we convert it into an audio file. ')
    elif message.text == 'Generate a random number':
        msg = bot.send_message(message.chat.id, 'Choose a number from 1 to 10')
        bot.register_next_step_handler(msg, randnum)
    elif message.text == 'Generate a complex password':
        symbols = digits + punctuation + ascii_letters
        sec_random = random.SystemRandom()
        hard_password = ''.join(sec_random.choice(symbols) for i in range(15))
        bot.send_message(message.chat.id, f'Your password:  {hard_password}')
    elif message.text == 'Generate a random ID':
        rand_id = uuid.uuid4()
        bot.send_message(message.chat.id, f'Your ID - {rand_id}')
    elif message.text == 'Convert text to audio':
        msg = bot.send_message(message.chat.id, 'What shall we convert??')
        bot.register_next_step_handler(msg, text_audio)
    else:
        pass


def randnum(message, user_result=None):
    try:
        global user_request

        if user_result == None:
            user_request = int(message.text)
        else:
            user_request = str(user_result)
        bot.send_message(message.chat.id, 'Well, let\'s check it out.')
        NumberToGuess = random.randint(1, 10)
        time.sleep(2)
        if user_request == NumberToGuess:
            bot.send_message(message.chat.id, f'Congratulations, you guessed it! It really was a number {NumberToGuess}')
        else:
            bot.send_message(message.chat.id, 'They didn\'t guess.\n Next time you will definitely be lucky!')
    except Exception:
        bot.reply_to(message, 'Error, try again')


def text_audio(message):
    bot.send_message(message.chat.id, 'I start the conversion process.')
    try:
        global user_request

        if user_result == None:
            user_request = str(message.text)
        else:
            user_request = str(user_result)

        audio = 'audio.mp3'
        language = 'en'
        sp = gTTS(text=user_request, lang=language, slow=False)
        sp.save(audio)
        bot.send_message(message.chat.id, 'Conversion completed successfully! I\'m dropping the audio.')
        audio_d = open("audio.mp3", 'rb')
        bot.send_audio(message.chat.id, audio_d)
    except Exception:
        bot.reply_to(message, "Something went wrong...")


bot.polling(none_stop=True)