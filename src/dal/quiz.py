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
