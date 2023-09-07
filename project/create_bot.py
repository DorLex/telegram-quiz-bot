import logging
from decouple import config
from aiogram import Bot, Dispatcher

from . import handlers
from . import custom_filters

API_TOKEN = config('API_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

custom_filters.register_filters(dispatcher)
handlers.register_handlers(dispatcher)
