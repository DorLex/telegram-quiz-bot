from aiogram import executor

from project.init_bot import dispatcher

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
