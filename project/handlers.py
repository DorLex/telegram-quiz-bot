from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from .database import db
from . import buttons
from .services import quiz_service
from .services import handler_service


async def send_welcome(message: types.Message):
    db.create_or_update_user(message.from_user.id, message.from_user.full_name)
    await message.answer('Привет! Готов проверить знания?', reply_markup=buttons.start_menu)


async def text_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        index_question = db.get_index_question(user_id)
        message_text = message.text

        if message_text == quiz_service.get_right_answer(index_question):
            await handler_service.add_point(user_id, index_question, message)

        elif message_text in quiz_service.get_answer_options(index_question):
            await handler_service.next_question(user_id, index_question, message)

        else:
            await message.answer('Нет такого варианта')

    except TypeError:
        await handler_service.end_quiz(message)


async def show_result(message: types.Message):
    await handler_service.get_result(message.from_user.id, message)


async def show_table_records(message: types.Message):
    await handler_service.get_table_records(message)


async def new_game(message: types.Message):
    await handler_service.reset_result(message.from_user.id, message)


async def start_quiz(message: types.Message):
    await handler_service.get_question(message.from_user.id, message)


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(send_welcome, commands=['start'])

    dispatcher.register_message_handler(start_quiz, Text(['Начать викторину', 'go']))
    dispatcher.register_message_handler(show_result, Text('Показать результат'))
    dispatcher.register_message_handler(show_table_records, Text('Показать таблицу рекордов'))
    dispatcher.register_message_handler(new_game, Text('Сыграть заново'))

    dispatcher.register_message_handler(text_handler)
