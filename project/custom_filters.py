from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from .database import db
from .services import data_service


class RightAnswerFilter(BoundFilter):
    key = 'right_answer'

    def __init__(self, right_answer):
        self.right_answer = right_answer

    async def check(self, message: types.Message) -> bool:
        index_question = db.get_index_question(message.from_user.id)
        return message.text == data_service.get_right_answer(index_question)


class InAnswerOptionsFilter(BoundFilter):
    key = 'in_answer_options'

    def __init__(self, in_answer_options):
        self.in_answer_options = in_answer_options

    async def check(self, message: types.Message) -> bool:
        index_question = db.get_index_question(message.from_user.id)
        return message.text in data_service.get_answer_options(index_question)


def register_filters(dispatcher):
    dispatcher.filters_factory.bind(RightAnswerFilter)
    dispatcher.filters_factory.bind(InAnswerOptionsFilter)
