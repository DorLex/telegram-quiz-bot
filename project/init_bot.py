import logging

from aiogram import Bot, Dispatcher
from decouple import config

from project import custom_filters, handlers

API_TOKEN = config('API_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

custom_filters.register_filters(dispatcher)
handlers.register_handlers(dispatcher)
