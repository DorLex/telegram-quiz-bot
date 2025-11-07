from aiogram.types import Message

from src.bll.dto.user import UserDTO
from src.bll.question import questions_loader
from src.dal.quiz import QuizRepository


class FilterService:
    def __init__(self, repository: QuizRepository) -> None:
        self.repository = repository

    async def is_right_answer(self, message: Message) -> dict | bool:
        user: UserDTO = await self.repository.get_user(message.from_user.id)
        right_answer: str = questions_loader.questions[user.question_id].right_answer

        if message.text == right_answer:
            return {'user': user}

        return False

    async def in_answer_options(self, message: Message) -> dict | bool:
        user: UserDTO = await self.repository.get_user(message.from_user.id)
        answer_options: list[str] = questions_loader.questions[user.question_id].answer_options

        if message.text in answer_options:
            return {'user': user}

        return False
