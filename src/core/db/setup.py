import aiosqlite
from aiosqlite import Connection

from src.core.constants import BASE_DIR


def connection_factory() -> Connection:
    return aiosqlite.connect(BASE_DIR / 'database.sqlite3')
