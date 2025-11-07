from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.bll.dto.question import Question
from src.bll.dto.user import UserDTO, UserResultDTO
from src.bll.question import questions_loader
from src.core.constants import END_MSG, START_MSG, EndKeyboardEnum
from src.dal.quiz import QuizRepository


class QuizService:
    def __init__(self, repository: QuizRepository) -> None:
        self.repository = repository

    async def is_right_answer(self, message: Message) -> bool:
        user: UserDTO = await self.repository.get_user(message.from_user.id)
        right_answer: str = questions_loader.questions[user.question_id].right_answer
        return message.text == right_answer

    async def in_answer_options(self, message: Message) -> bool:
        user: UserDTO = await self.repository.get_user(message.from_user.id)
        answer_options: list[str] = questions_loader.questions[user.question_id].answer_options
        return message.text in answer_options

    async def add_gamer(self, message: Message) -> None:
        await self.repository.create_or_update_user(message.from_user.id, message.from_user.full_name)

    async def get_current_question(self, message: Message) -> tuple[str, ReplyKeyboardMarkup]:
        user: UserDTO = await self.repository.get_user(message.from_user.id)

        question: Question = questions_loader.questions[user.question_id]
        keyboard: ReplyKeyboardMarkup = self._build_keyboard(question.answer_options)

        return question.text, keyboard

    async def add_point(self, message: Message) -> tuple[str, ReplyKeyboardMarkup]:
        await self.repository.add_point(message.from_user.id)
        return await self.next_question(message)

    async def next_question(self, message: Message) -> tuple[str, ReplyKeyboardMarkup]:
        user: UserDTO = await self.repository.get_user(message.from_user.id)

        if user.question_id >= len(questions_loader.questions) - 1:
            keyboard: ReplyKeyboardMarkup = self._get_end_keyboard()
            return END_MSG, keyboard

        await self.repository.increase_question_id(message.from_user.id)
        return await self.get_current_question(message)

    async def show_result(self, message: Message) -> tuple[str, ReplyKeyboardMarkup]:
        user: UserDTO = await self.repository.get_user(message.from_user.id)

        result: str = f'🧮 Правильно {user.score} из {len(questions_loader.questions)}'
        keyboard: ReplyKeyboardMarkup = self._get_end_keyboard()

        return result, keyboard

    async def show_leaderboard(self) -> tuple[str, ReplyKeyboardMarkup]:
        top_10_users_result: list[UserResultDTO] = await self.repository.get_top_10_users_result()

        leaderboard: str = '🏆\n'
        num_place = 1
        for result in top_10_users_result:
            leaderboard += f'{num_place}. {result.name}: {result.score}\n'
            num_place += 1

        keyboard: ReplyKeyboardMarkup = self._get_end_keyboard()
        return leaderboard, keyboard

    async def new_game(self, message: Message) -> tuple[str, ReplyKeyboardMarkup]:
        await self.repository.reset_user_progress(message.from_user.id)

        text: str = '0️⃣ Счет обнулён. Желаете сыграть еще раз?'
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
