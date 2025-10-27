from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.core.constants import END_MSG, START_MSG, EndKeyboardEnum
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

    async def get_current_question(self, message: Message) -> tuple[str, ReplyKeyboardMarkup]:
        question_id: int = db.get_current_question_id(message.from_user.id)

        text_question: str = questions_and_answers.get(question_id)['text']
        answer_options: list[str] = questions_and_answers.get(question_id)['answer_options']

        keyboard: ReplyKeyboardMarkup = self._build_keyboard(answer_options)

        return text_question, keyboard

    async def add_point(self, message: Message) -> tuple[str, ReplyKeyboardMarkup]:
        db.add_point(message.from_user.id)
        return await self.next_question(message)

    async def next_question(self, message: Message) -> tuple[str, ReplyKeyboardMarkup]:
        question_id: int = db.get_current_question_id(message.from_user.id)
        if question_id >= len(questions_and_answers) - 1:
            keyboard: ReplyKeyboardMarkup = self._get_end_keyboard()
            return END_MSG, keyboard

        db.update_question_id(message.from_user.id)
        return await self.get_current_question(message)

    async def show_result(self, message: Message) -> tuple[str, ReplyKeyboardMarkup]:
        score: int = db.get_score(message.from_user.id)
        result: str = f'Правильно {score} из {len(questions_and_answers)}'
        keyboard: ReplyKeyboardMarkup = self._get_end_keyboard()

        return result, keyboard

    async def show_leaderboard(self) -> tuple[str, ReplyKeyboardMarkup]:
        top_10_users_results: list[tuple] = db.get_top_10_users_results()

        leaderboard: str = ''
        num_place = 1
        for user_name, score in top_10_users_results:
            leaderboard += f'{num_place}. {user_name} : {score}\n'
            num_place += 1

        keyboard: ReplyKeyboardMarkup = self._get_end_keyboard()

        return leaderboard, keyboard

    async def new_game(self, message: Message) -> tuple[str, ReplyKeyboardMarkup]:
        db.reset_user_score(message.from_user.id)
        db.reset_index_question(message.from_user.id)

        text: str = 'Счет обнулён. Желаете сыграть еще раз?'
        keyboard = self.get_welcome_keyboard()

        return text, keyboard

    def _build_keyboard(self, button_texts: list[str]) -> ReplyKeyboardMarkup:
        keyboard_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

        for text in button_texts:
            keyboard_builder.button(text=text)
        keyboard_builder.adjust(1)

        return keyboard_builder.as_markup(
            resize_keyboard=True,
            input_field_placeholder='Выберите вариант:',  # подсказка в поле ввода
        )

    def get_welcome_keyboard(self) -> ReplyKeyboardMarkup:
        return self._build_keyboard([START_MSG])

    def _get_end_keyboard(self) -> ReplyKeyboardMarkup:
        return self._build_keyboard(
            [
                EndKeyboardEnum.show_result,
                EndKeyboardEnum.show_leaderboard,
                EndKeyboardEnum.new_game,
            ],
        )
