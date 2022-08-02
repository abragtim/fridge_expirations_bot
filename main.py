import asyncio
import datetime
from telebot.async_telebot import AsyncTeleBot

token = '5158749767:AAFSWeTIXiyZku20Ffh8X7jGcg9qHgepetU'
bot = AsyncTeleBot(token)

#TODO: comments
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, "Hi! Use /set <seconds> to set a timer")


@bot.message_handler(commands=['set'])
async def set_timer(message):
    args = message.text.split()
    if len(args) > 2:
        user = message.chat.id
        await expiration_timer(args[1], args[2], user)
    else:
        await bot.reply_to(message, 'Usage: /set <product> <expiration date>')


async def expiration_timer(product: str, date: str, user):
    print(product, date) #TODO: change (to logger mb)
    date = date.split('.')
    if len(date) < 3:
        assert False, 'Wrong date format'
    try:
        date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]))
    except TypeError:
        assert False, 'Wrong year/month/day format'
    date_delta = date - datetime.datetime.today()
    timer = date_delta.days * 24 * 60 + date_delta.seconds
    await asyncio.sleep(timer)
    await bot.send_message(user, f"Don't eat {product}!")


asyncio.run(bot.polling())
