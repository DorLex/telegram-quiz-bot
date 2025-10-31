import aiosqlite
from aiosqlite import Connection

from src.core.constants import BASE_DIR

connection: Connection = aiosqlite.connect(BASE_DIR / 'database.db')
