from aiosqlite import Connection

from src.bll.dto.user import UserDTO


class QuizRepository:
    def __init__(self, db: Connection) -> None:
        self.db = db

    async def get_user(self, user_id: int) -> UserDTO:
        query: str = """
            SELECT *
              FROM user
              WHERE id == (?);
            """
        params: tuple = (user_id,)

        async with self.db.execute(query, params) as cursor:
            result: dict | None = await cursor.fetchone()

        # TODO вызвать исключение, когда result=None

        return UserDTO(**result)

    async def get_top_10_users_result(self) -> list[dict]:
        query: str = """
            SELECT name, score
              FROM user
              ORDER BY score DESC
              LIMIT 10;
            """

        async with self.db.execute(query) as cursor:
            result: list[dict] | None = await cursor.fetchall()

        return result
