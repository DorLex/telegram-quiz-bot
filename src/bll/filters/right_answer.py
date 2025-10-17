from aiogram.filters import Filter
from aiogram.types import Message

from src.bll.quiz import QuizService


class RightAnswerFilter(Filter):
    async def __call__(self, message: Message) -> dict | bool:
        quiz_service: QuizService = QuizService()
        return await quiz_service.is_right_answer(message)
