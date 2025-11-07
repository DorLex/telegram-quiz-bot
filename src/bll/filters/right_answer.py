from aiogram.filters import Filter
from aiogram.types import Message

from src.bll.filter import FilterService
from src.core.db.logs import log_query
from src.core.db.setup import connection_factory, row_dict_factory
from src.dal.quiz import QuizRepository


class RightAnswerFilter(Filter):
    async def __call__(self, message: Message) -> dict | bool:
        async with connection_factory() as db:
            db.row_factory = row_dict_factory
            await db.set_trace_callback(log_query)

            filter_service: FilterService = FilterService(QuizRepository(db))
            result: dict | bool = await filter_service.is_right_answer(message)

        return result
