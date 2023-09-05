import logging

from aiogram import executor

from project.create_bot import dp
from project import handlers

logging.basicConfig(level=logging.INFO)

handlers.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
