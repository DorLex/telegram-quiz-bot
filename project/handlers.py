from aiogram import types, Dispatcher

from .database import db
from . import buttons
from . import quiz


async def send_welcome(message: types.Message):
    await message.answer('Привет! Готов проверить знания?', reply_markup=buttons.start_menu)
    db.create_or_update_user(message.from_user.id, message.from_user.full_name)


async def text_handler(message: types.Message):
    try:
        if message.text == 'Показать результат':
            answer_text = f'Правильно {db.get_score(message.from_user.id)} из 10'
            await message.answer(answer_text, reply_markup=buttons.end_menu)

        elif message.text == 'Показать таблицу рекордов':
            await message.answer(db.get_table_records(), reply_markup=buttons.end_menu)

        elif message.text == 'Сыграть заново':
            db.reset_score(message.from_user.id)
            db.reset_index_question(message.from_user.id)
            await message.answer('Счет обнулён. Желаете сыграть еще раз?', reply_markup=buttons.start_menu)

        elif message.text == 'Начать викторину':
            text_question, answer_options_keyboard = quiz.generate_question(message.from_user.id)
            await message.answer(text_question, reply_markup=answer_options_keyboard)

        elif message.text == quiz.get_right_answer(message.from_user.id):
            db.update_score(message.from_user.id)
            db.update_index_question(message.from_user.id)
            text_question, answer_options_keyboard = quiz.generate_question(message.from_user.id)

            await message.answer(text_question, reply_markup=answer_options_keyboard)

        elif message.text in quiz.get_answer_options(db.get_index_question(message.from_user.id)):
            db.update_index_question(message.from_user.id)
            text_question, answer_options_keyboard = quiz.generate_question(message.from_user.id)

            await message.answer(text_question, reply_markup=answer_options_keyboard)

        else:
            await message.answer('Нет такого варианта')

    except TypeError:
        await message.answer('Вы прошли викторину.', reply_markup=buttons.end_menu)


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(send_welcome, commands=['start'])
    dispatcher.register_message_handler(text_handler)
