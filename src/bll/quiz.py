from aiogram.types import Message

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
