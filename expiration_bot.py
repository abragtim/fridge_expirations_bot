import asyncio
import datetime
from telebot.async_telebot import AsyncTeleBot
from logger import logger


def bot_server(token):
    ''' Main process. Activating bot '''
    bot = AsyncTeleBot(token)  # you can get token from BotFather


    @bot.message_handler(commands=['help', 'start'])
    async def send_welcome(message):
        ''' Handle /help or /start command. '''
        await bot.reply_to(message,
                           "Hi! Use <product> <expiration date> to set an expiration date for product")


    @bot.message_handler(content_types=['text'])
    async def set_timer(message):
        ''' Handle setting. '''
        args = message.text.split()
        if len(args) > 1:
            user = message.chat.id  # get's tg secured chat's id with user
            await expiration_timer(args[0], args[1], user)
        else:
            await bot.reply_to(message, 'Usage: <product> <expiration date>')



    async def expiration_timer(product: str, date: str, user):
        ''' Seting an expiration timer by user for product on current date. '''
        logger.info(f"User {user} request set {date} for {product}.")

        date = date.split('.')  # str -> list
        if len(date) < 3:
            # need at leatst 3 args for setting
            await bot.send_message(
                user,
                'Usage: <product> <expiration date>. Format of date is D.M.Y')
            logger.error(f"wrong request: expiration date {date} for {product} by user = {user}")

        try:
            date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]))
        except TypeError:
            # srong format of data (need D.M.Y)
            await bot.send_message(
                user,
                'Wrong year/month/day format. Correct: D.M.Y (exapmle: 3.1.2022)')
            logger.error(f'Wrong year/month/day format: user = {user}, product = {product}, date = {date}')

        date_delta = date - datetime.datetime.today()  # days before expire
        # datetime -> int (seconds)
        timer = date_delta.days * 24 * 60 + date_delta.seconds
        await bot.send_message(user, f'The notification for {product} is set for {date}.')
        await asyncio.sleep(timer)
        await bot.send_message(user, f"Don't eat {product}!")  # beep!


    asyncio.run(bot.infinity_polling())  # bot activating
