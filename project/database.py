import sqlite3 as sql
from sqlite3 import Cursor


class Database:
    def __init__(self, db_file: str) -> None:
        with sql.connect(db_file) as self.database:
            self.cursor: Cursor = self.database.cursor()
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                index_question INTEGER NOT NULL DEFAULT 0,
                score INTEGER NOT NULL DEFAULT 0
                );
                """
            )

    def create_or_update_user(self, user_id: int, user_name: str) -> None:
        with self.database:
            self.cursor.execute(
                """
                INSERT INTO users (id, name) VALUES (?, ?)
                ON CONFLICT (id) DO
                UPDATE SET name = (?);
                """,
                (user_id, user_name, user_name,)
            )

    def get_index_question(self, user_id: int) -> int:
        with self.database:
            self.cursor.execute(
                """
                SELECT index_question 
                FROM users 
                WHERE id == (?);
                """,
                (user_id,)
            )

            index_question: int = self.cursor.fetchone()[0]
            return index_question

    def update_index_question(self, user_id: int) -> None:
        with self.database:
            self.cursor.execute(
                """
                UPDATE users 
                SET index_question = index_question + 1 
                WHERE id == (?);
                """,
                (user_id,)
            )

    def reset_index_question(self, user_id: int) -> None:
        with self.database:
            self.cursor.execute(
                """
                UPDATE users 
                SET index_question = (?) 
                WHERE id == (?);
                """,
                (0, user_id,)
            )

    def get_score(self, user_id: int) -> int:
        with self.database:
            self.cursor.execute(
                """
                SELECT score 
                FROM users 
                WHERE id == (?);
                """,
                (user_id,)
            )

            score: int = self.cursor.fetchone()[0]
            return score

    def update_score(self, user_id: int) -> None:
        with self.database:
            self.cursor.execute(
                """
                UPDATE users 
                SET score = score + 1 
                WHERE id == (?);
                """,
                (user_id,)
            )

    def reset_user_score(self, user_id: int) -> None:
        with self.database:
            self.cursor.execute(
                """
                UPDATE users 
                SET score = (?) 
                WHERE id == (?);
                """,
                (0, user_id,)
            )

    def get_top_10_users_results(self) -> list[tuple]:
        with self.database:
            self.cursor.execute(
                """
                SELECT name, score 
                FROM users 
                ORDER BY score DESC
                LIMIT 10;
                """
            )

            results: list[tuple] = self.cursor.fetchall()
            return results


db = Database('database.db')
