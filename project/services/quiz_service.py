from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from project.questions import questions_and_answers


def get_text_question(index_question):
    text_question = questions_and_answers.get(index_question)['text']
    return text_question


def get_answer_options(index_question):
    answer_options = questions_and_answers.get(index_question)['answer_options']
    return answer_options


def get_right_answer(index_question):
    right_answer = questions_and_answers.get(index_question)['right_answer']
    return right_answer


def generate_options_keyboard(answer_options):
    answer_options_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for option in answer_options:
        answer_options_keyboard.add(KeyboardButton(option))

    return answer_options_keyboard


def generate_question(index_question):
    text_question = get_text_question(index_question)
    answer_options = get_answer_options(index_question)

    answer_options_keyboard = generate_options_keyboard(answer_options)

    return text_question, answer_options_keyboard
