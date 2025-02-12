from aiogram import Dispatcher
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from project.database import db
from project.services import questions


class RightAnswerFilter(BoundFilter):
    key = 'right_answer'

    def __init__(self, right_answer: bool) -> None:
        self.right_answer = right_answer

    async def check(self, message: Message) -> bool:
        index_question: int = db.get_index_question(message.from_user.id)
        return message.text == questions.get_right_answer(index_question)


class InAnswerOptionsFilter(BoundFilter):
    key = 'in_answer_options'

    def __init__(self, in_answer_options: bool) -> None:
        self.in_answer_options = in_answer_options

    async def check(self, message: Message) -> bool:
        index_question: int = db.get_index_question(message.from_user.id)
        return message.text in questions.get_answer_options(index_question)


def register_filters(dispatcher: Dispatcher) -> None:
    dispatcher.filters_factory.bind(RightAnswerFilter)
    dispatcher.filters_factory.bind(InAnswerOptionsFilter)
