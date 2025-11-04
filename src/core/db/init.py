from aiosqlite import Cursor

from src.core.db.logs import log_query
from src.core.db.setup import connection_factory


async def init_db() -> None:
    async with connection_factory() as db:
        await db.set_trace_callback(log_query)

        query: str = """
            CREATE TABLE IF NOT EXISTS user (
              id INTEGER PRIMARY KEY,
              name TEXT NOT NULL,
              question_id INTEGER NOT NULL DEFAULT 0,
              score INTEGER NOT NULL DEFAULT 0
            );
            """

        async with db.execute(query) as cursor:
            cursor: Cursor
            await cursor.execute(query)
