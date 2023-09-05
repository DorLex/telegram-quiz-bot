import logging
from decouple import config
from aiogram import Bot, Dispatcher

from project import handlers

API_TOKEN = config('API_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

handlers.register_handlers(dispatcher)
