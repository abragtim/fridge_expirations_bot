import imp
import telebot
from datetime import datetime

bot = telebot.TeleBot("5158749767:AAFSWeTIXiyZku20Ffh8X7jGcg9qHgepetU")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hello')


#TODO: add
bot.infinity_polling()
