import datetime, time, asyncio
from telebot.async_telebot import AsyncTeleBot
from logger import logger


async def reconnect(bot: AsyncTeleBot, requests):
    ''' Reconnection after server restarting. '''

    async def continue_timer(request):
        ''' Continue timer to expiration date for product '''
        user = int(request[0])
        product = str(request[1])
        date = _from_str_to_datetime(request[2])
        logger.info(f'Reconnection: user = {user}, product = {product}, date = {date}')
        # sleep
        timer = (date - datetime.datetime.today()).total_seconds()
        await asyncio.sleep(timer)
        # waking up
        await bot.send_message(user, 'Reconnection test') #TODO: change

    def sort_requests_key(request):
        ''' Key function for request.sort(): sorting according to exp. date'''
        date = _from_str_to_datetime(request[2])
        return date

    request = requests.sort(key=sort_requests_key)
    for request in requests:
        # continue timer for request
        await continue_timer(request)
        # TODO: delete from db


def _from_str_to_datetime(string: str) -> datetime:
    date = string.split(' ')[0].split('-')
    date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
    return date
