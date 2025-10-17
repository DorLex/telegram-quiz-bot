from aiogram.filters import Filter
from aiogram.types import Message

from src.bll.quiz import QuizService


class InAnswerOptionsFilter(Filter):
    async def __call__(self, message: Message) -> dict | bool:
        quiz_service: QuizService = QuizService()
        return await quiz_service.in_answer_options(message)
