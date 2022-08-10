import asyncio, datetime, sqlite3
from logger import logger
from threading import Thread
from telebot.async_telebot import AsyncTeleBot
from telebot import TeleBot
from reconnection import reconnect


def bot_server(token):
    ''' Main process. Activating bot '''

    bot = AsyncTeleBot(token)  # you can get token from BotFather

    # database activating
    db = sqlite3.connect('requests.db')
    cur = db.cursor()
    try:
        # table doesn't exist
        cur.execute('''CREATE TABLE requests (user, product, date)''')
    except sqlite3.OperationalError:
        # table exists, reconnect
        requests = [request for request in cur.execute('''SELECT * FROM requests''')]
        th = Thread(target=reconnect, args=(token, requests))
        th.start()
    db.commit()
    #TODO: mb db.reconnect() method create


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
        date = date.split('.')  # str -> list
        if len(date) < 3:
            # need at leatst 3 args for setting
            await bot.send_message(
                user,
                'Usage: <product> <expiration date>. Format of date is D.M.Y')
        try:
            date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]))
        except TypeError:
            # srong format of data (need D.M.Y)
            await bot.send_message(
                user,
                'Wrong year/month/day format. Correct: D.M.Y (exapmle: 3.1.2022)')
        date_delta = date - datetime.datetime.today()  # days before expire
        # datetime -> int (seconds)
        timer = date_delta.days * 24 * 60 + date_delta.seconds

        # adding values to database
        cur.execute('''INSERT INTO requests VALUES ('{}', '{}', '{}')'''.format(user, product, date))
        db.commit()
        # TODO: logger need or not?
        logger.info(f'User {user} notificate {product} on {date}.')
        await bot.send_message(user, f'Notification for {product} seted on {date}.')
        await asyncio.sleep(timer)
        await bot.send_message(user, f"Don't eat {product}!")  # beep!
        #TODO: delete from db values


    asyncio.run(bot.infinity_polling())  # bot activating

    db.close()


bot_server('5445553488:AAHEdWMPG76Lx0E4Wp4hQ51aSpvauxA9K3w')