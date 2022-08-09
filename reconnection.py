import datetime, time
from telebot import TeleBot
from logger import logger


def reconnect(token, requests):
    ''' Reconnection after server restarting. '''
    admin_bot = TeleBot(token=token)

    def continue_timer(request):
        ''' Continue timer to expiration date for product '''
        user = request[0]
        product = request[1]
        date = _from_str_to_datetime(request[2])
        logger.info(f'Reconnection: user = {user}, product = {product}, date = {date}')
        # sleep
        date_delta = date - datetime.datetime.today()
        timer = date_delta.days * 24 * 60 + date_delta.seconds
        time.sleep(timer)
        # waking up
        admin_bot.send_message(user, 'Reconnection test') #TODO: change

    def sort_requests_key(request):
        ''' Key function for request.sort(): sorting according to exp. date'''
        date = _from_str_to_datetime(request[2])
        return date

    request = requests.sort(key=sort_requests_key)
    for request in requests:
        # continue timer for request
        continue_timer(request)
        # TODO: delete from db


def _from_str_to_datetime(string: str) -> datetime:
    date = string.split(' ')[0].split('-')
    date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
    return date
