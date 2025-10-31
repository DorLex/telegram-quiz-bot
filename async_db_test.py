import asyncio
import logging
from logging import Logger, getLogger

import aiosqlite
from aiosqlite import Connection, Cursor

logging.basicConfig(level=logging.INFO)

logger: Logger = getLogger(__name__)


def log_query(query: str) -> None:
    logger.info(f'Выполняется SQL: {query}')


async def main() -> None:
    connection: Connection = aiosqlite.connect('database.sqlite3')

    async with connection as conn:
        conn: Connection

        await conn.set_trace_callback(log_query)

        query: str = """
            SELECT * FROM users
        """

        async with conn.execute(query) as cursor:
            cursor: Cursor
            async for row in cursor:
                logger.info(row)

        # async with conn.execute(query) as cursor:
        #     rows: list[tuple] = await cursor.fetchall()


if __name__ == '__main__':
    asyncio.run(main())
