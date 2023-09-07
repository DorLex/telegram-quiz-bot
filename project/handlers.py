from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from .services import handler_service


async def welcome(message: types.Message):
    await handler_service.add_gamer(message)


async def start_quiz(message: types.Message):
    await handler_service.get_question(message.from_user.id, message)


async def show_result(message: types.Message):
    await handler_service.get_result(message.from_user.id, message)


async def show_table_records(message: types.Message):
    await handler_service.get_table_records(message)


async def new_game(message: types.Message):
    await handler_service.reset_result(message.from_user.id, message)


async def right_answer(message: types.Message):
    await handler_service.add_point(message.from_user.id, message)


async def wrong_answer(message: types.Message):
    await handler_service.next_question(message.from_user.id, message)


async def random_text_handler(message: types.Message):
    await message.answer('Нет такого варианта')


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(welcome, commands=['start'])

    dispatcher.register_message_handler(start_quiz, Text(['Начать викторину', 'go']))

    dispatcher.register_message_handler(right_answer, right_answer=True)
    dispatcher.register_message_handler(wrong_answer, in_answer_options=True)

    dispatcher.register_message_handler(show_result, Text('Показать результат'))
    dispatcher.register_message_handler(show_table_records, Text('Показать таблицу рекордов'))
    dispatcher.register_message_handler(new_game, Text(['Сыграть заново', 'r']))

    dispatcher.register_message_handler(random_text_handler)
