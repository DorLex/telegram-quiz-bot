from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

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

    def _generate_keyboard(self, button_grid: list[list[KeyboardButton]]) -> ReplyKeyboardMarkup:
        keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            keyboard=button_grid,
            resize_keyboard=True,
            input_field_placeholder='Выберите вариант:',  # подсказка в поле ввода
        )

        return keyboard

    async def get_kb(self) -> ReplyKeyboardMarkup:
        button: KeyboardButton = KeyboardButton(text='Начать викторину')

        button_grid: list[list[KeyboardButton]] = [
            [button],
        ]

        return self._generate_keyboard(button_grid)
