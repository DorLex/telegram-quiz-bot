from aiogram.types import Message

from project import buttons
from project.database import db
from project.questions import questions_and_answers
from project.services import questions


async def add_gamer(message: Message) -> None:
    db.create_or_update_user(message.from_user.id, message.from_user.full_name)
    await message.answer('Привет! Готов проверить знания?', reply_markup=buttons.start_menu)


async def get_question(user_id: int, message: Message) -> Message:
    index_question: int = db.get_index_question(user_id)
    text_question, answer_options_keyboard = questions.generate_question(index_question)

    return await message.answer(text_question, reply_markup=answer_options_keyboard)


async def get_result(user_id: int, message: Message) -> Message:
    answer_text: str = f'Правильно {db.get_score(user_id)} из {len(questions_and_answers)}'
    return await message.answer(answer_text, reply_markup=buttons.end_menu)


async def get_table_records(message: Message) -> Message:
    top_10_users_results: list[tuple] = db.get_top_10_users_results()

    table_records = ''
    num_place = 1
    for user_name, score in top_10_users_results:
        table_records += f'{num_place}. {user_name} : {score}\n'
        num_place += 1

    return await message.answer(table_records, reply_markup=buttons.end_menu)


async def reset_result(user_id: int, message: Message) -> Message:
    db.reset_user_score(user_id)
    db.reset_index_question(user_id)
    return await message.answer('Счет обнулён. Желаете сыграть еще раз?', reply_markup=buttons.start_menu)


async def next_question(user_id: int, message: Message) -> Message:
    index_question: int = db.get_index_question(user_id)
    if questions.next_index_out_of_range(index_question):
        return await end_quiz(message)

    db.update_index_question(user_id)

    return await get_question(user_id, message)


async def add_point(user_id: int, message: Message) -> Message:
    db.update_score(user_id)
    return await next_question(user_id, message)


async def end_quiz(message: Message) -> Message:
    return await message.answer('Вы прошли викторину!', reply_markup=buttons.end_menu)
