from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.core.constants import START_MSG, EndKeyboardEnum
from src.database import db
from src.questions import questions_and_answers


class QuizService:
    async def is_right_answer(self, message: Message) -> bool:
        question_id: int = db.get_current_question_id(message.from_user.id)
        right_answer: str = questions_and_answers.get(question_id)['right_answer']
        return message.text == right_answer

    async def in_answer_options(self, message: Message) -> bool:
        question_id: int = db.get_current_question_id(message.from_user.id)
        answer_options: list[str] = questions_and_answers.get(question_id)['answer_options']
        return message.text in answer_options

    async def add_gamer(self, message: Message) -> None:
        db.create_or_update_user(message.from_user.id, message.from_user.full_name)

    def get_welcome_keyboard(self) -> ReplyKeyboardMarkup:
        return self._build_keyboard([START_MSG])

    def _build_keyboard(self, button_texts: list[str]) -> ReplyKeyboardMarkup:
        keyboard_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

        for text in button_texts:
            keyboard_builder.button(text=text)
        keyboard_builder.adjust(1)

        return keyboard_builder.as_markup(
            resize_keyboard=True,
            input_field_placeholder='Выберите вариант:',  # подсказка в поле ввода
        )

    async def get_current_question(self, message: Message) -> tuple[str, ReplyKeyboardMarkup]:
        question_id: int = db.get_current_question_id(message.from_user.id)

        text_question: str = questions_and_answers.get(question_id)['text']
        answer_options: list[str] = questions_and_answers.get(question_id)['answer_options']

        keyboard: ReplyKeyboardMarkup = self._build_keyboard(answer_options)

        return text_question, keyboard

    async def show_result(self, message: Message) -> tuple[str, ReplyKeyboardMarkup]:
        score: int = db.get_score(message.from_user.id)

        result: str = f'Правильно {score} из {len(questions_and_answers)}'

        keyboard: ReplyKeyboardMarkup = self._build_keyboard(
            [
                EndKeyboardEnum.show_result,
                EndKeyboardEnum.show_leaderboard,
                EndKeyboardEnum.new_game,
            ],
        )

        return result, keyboard
