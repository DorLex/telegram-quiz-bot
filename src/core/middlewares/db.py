from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from src.core.db.logs import log_query
from src.core.db.setup import connection_factory, row_dict_factory


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        async with connection_factory() as db:
            db.row_factory = row_dict_factory
            await db.set_trace_callback(log_query)

            data['db'] = db

            result: Any = await handler(event, data)

        return result
