from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from src.bll.utils.db.logs import log_query
from src.core.db.setup import connection_factory


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        async with connection_factory() as conn:
            await conn.set_trace_callback(log_query)
            data['db'] = conn

            result: Any = await handler(event, data)

        return result
