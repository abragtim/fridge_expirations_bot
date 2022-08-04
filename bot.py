import asyncio
import datetime
from telebot.async_telebot import AsyncTeleBot
from logs import my_logger


def bot_server(token):
    ''' Main function. Activating bot '''
    global bot
    bot = AsyncTeleBot(token)
    asyncio.run(bot.polling())

# TODO: where to work with main func???
bot_server('5158749767:AAFSWeTIXiyZku20Ffh8X7jGcg9qHgepetU')


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    ''' Handle /help or /start command. '''
    await bot.reply_to(message,
                       "Hi! Use /set <product> <expiration date> to set an expiration date for product")


@bot.message_handler(commands=['set'])
async def set_timer(message):
    ''' Handle /set command. '''
    args = message.text.split()
    if len(args) > 2:
        user = message.chat.id  # get's tg secured chat's id with user
        await expiration_timer(args[1], args[2], user)
    else:
        await bot.reply_to(message, 'Usage: /set <product> <expiration date>')


async def expiration_timer(product: str, date: str, user):
    ''' Seting an expiration timer by user for product on current date. '''
    my_logger.logger(("user's request", user, product, date))
    date = date.split('.')  # str -> list
    if len(date) < 3:
        # need at leatst 3 args for /set
        bot.send_message(
            user,
            'Usage: /set <product> <expiration date>. Format of date is D.M.Y')
        my_logger.logger(('error', user, product, date, 'wrong date format'))
    try:
        date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]))
    except TypeError:
        # srong format of data (need D.M.Y)
        bot.send_message(
            user,
            'Wrong year/month/day format. Correct: D.M.Y (exapmle: 3.1.2022)')
        my_logger.logger('error', user, product, date,
                         'Wrong year/month/day format')
    date_delta = date - datetime.datetime.today()  # days before expire
    # datetime -> int (seconds)
    timer = date_delta.days * 24 * 60 + date_delta.seconds
    bot.send_message(user, f'Notification for {product} seted on {date}.')
    await asyncio.sleep(timer)
    await bot.send_message(user, f"Don't eat {product}!")  # beep!

