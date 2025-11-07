from typing import Any

import aiosqlite
from aiosqlite import Connection, Cursor

from src.core.constants import BASE_DIR


def connection_factory() -> Connection:
    return aiosqlite.connect(BASE_DIR / 'database.sqlite3')


def row_dict_factory(cursor: Cursor, row: tuple) -> dict[str, Any]:
    """Из документации sqlite3"""

    fields: list[str] = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}
