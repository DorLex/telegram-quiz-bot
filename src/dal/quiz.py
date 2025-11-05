from aiosqlite import Connection

from src.bll.dto.user import UserDTO


class QuizRepository:
    def __init__(self, db: Connection) -> None:
        self.db = db

    async def create_or_update_user(self, user_id: int, user_name: str) -> None:
        query: str = """
            INSERT INTO user (id, name)
              VALUES (:id, :name)
              ON CONFLICT (id) DO
                UPDATE SET name = :name;
            """
        params: dict = {'id': user_id, 'name': user_name}

        await self.db.execute(query, params)
        await self.db.commit()

    async def get_user(self, user_id: int) -> UserDTO:
        query: str = """
            SELECT *
              FROM user
              WHERE id == :id;
            """
        params: dict = {'id': user_id}

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

    async def increase_question_id(self, user_id: int) -> None:
        query: str = """
            UPDATE user
              SET question_id = question_id + 1
              WHERE id == :id;
            """
        params: dict = {'id': user_id}

        await self.db.execute(query, params)
        await self.db.commit()

    async def reset_question_id(self, user_id: int) -> None:
        query: str = """
            UPDATE user
              SET question_id = :question_id
              WHERE id == :id;
            """
        params: dict = {'question_id': 0, 'id': user_id}

        await self.db.execute(query, params)
        await self.db.commit()
