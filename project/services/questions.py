from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from project.questions import questions_and_answers


def next_index_out_of_range(index_question: int) -> bool:
    if index_question >= len(questions_and_answers) - 1:
        return True
    return False


def _get_text_question(index_question: int) -> str:
    return questions_and_answers.get(index_question)['text']


def get_answer_options(index_question: int) -> list[str]:
    return questions_and_answers.get(index_question)['answer_options']


def get_right_answer(index_question: int) -> str:
    return questions_and_answers.get(index_question)['right_answer']


def _generate_options_keyboard(answer_options: list[str]) -> ReplyKeyboardMarkup:
    answer_options_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for option in answer_options:
        answer_options_keyboard.add(KeyboardButton(option))

    return answer_options_keyboard


def generate_question(index_question: int) -> tuple[str, ReplyKeyboardMarkup]:
    text_question: str = _get_text_question(index_question)
    answer_options: list[str] = get_answer_options(index_question)

    answer_options_keyboard: ReplyKeyboardMarkup = _generate_options_keyboard(answer_options)

    return text_question, answer_options_keyboard
