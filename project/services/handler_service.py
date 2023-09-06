from aiogram import types

from project import buttons
from project.database import db
from . import quiz_service


async def get_result(user_id: int, message: types.Message):
    answer_text = f'Правильно {db.get_score(user_id)} из 10'
    await message.answer(answer_text, reply_markup=buttons.end_menu)


async def get_table_records(message: types.Message):
    results: list[tuple] = db.get_users_results()

    table_records = ''
    num_place = 1
    for user_name, score in results:
        table_records += f'{num_place}. {user_name} : {score}\n'
        num_place += 1

    await message.answer(table_records, reply_markup=buttons.end_menu)


async def reset_result(user_id: int, message: types.Message):
    db.reset_user_score(user_id)
    db.reset_index_question(user_id)
    await message.answer('Счет обнулён. Желаете сыграть еще раз?', reply_markup=buttons.start_menu)


async def get_question(user_id: int, message: types.Message):
    index_question = db.get_index_question(user_id)
    text_question, answer_options_keyboard = quiz_service.generate_question(index_question)

    await message.answer(text_question, reply_markup=answer_options_keyboard)


async def add_point(user_id, index_question, message):
    db.update_score(user_id)
    db.update_index_question(user_id)

    text_question, answer_options_keyboard = quiz_service.generate_question(index_question + 1)

    await message.answer(text_question, reply_markup=answer_options_keyboard)


async def next_question(user_id, index_question, message):
    db.update_index_question(user_id)
    text_question, answer_options_keyboard = quiz_service.generate_question(index_question + 1)

    await message.answer(text_question, reply_markup=answer_options_keyboard)


async def end_quiz(message):
    await message.answer('Вы прошли викторину.', reply_markup=buttons.end_menu)
