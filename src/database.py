import sqlite3 as sql
from sqlite3 import Connection, Cursor


class Database:
    def __init__(self, db_file: str) -> None:
        self.conn: Connection = sql.connect(db_file)

        with self.conn:
            self.cursor: Cursor = self.conn.cursor()

        #     self.cursor.execute(
        #         """
        #         CREATE TABLE IF NOT EXISTS user (
        #           id INTEGER PRIMARY KEY,
        #           name TEXT NOT NULL,
        #           question_id INTEGER NOT NULL DEFAULT 0,
        #           score INTEGER NOT NULL DEFAULT 0
        #         );
        #         """,
        #     )

    # def create_or_update_user(self, user_id: int, user_name: str) -> None:
    #     with self.conn:
    #         self.cursor.execute(
    #             """
    #             INSERT INTO user (id, name) VALUES (?, ?)
    #               ON CONFLICT (id) DO
    #               UPDATE SET name = (?);
    #             """,
    #             (user_id, user_name, user_name),
    #         )

    # def get_current_question_id(self, user_id: int) -> int:
    #     with self.conn:
    #         self.cursor.execute(
    #             """
    #             SELECT question_id
    #               FROM user
    #               WHERE id == (?);
    #             """,
    #             (user_id,),
    #         )
    #
    #         question_id: int = self.cursor.fetchone()[0]
    #     return question_id

    # def update_question_id(self, user_id: int) -> None:
    #     with self.conn:
    #         self.cursor.execute(
    #             """
    #             UPDATE user
    #               SET question_id = question_id + 1
    #               WHERE id == (?);
    #             """,
    #             (user_id,),
    #         )

    # def reset_question_id(self, user_id: int) -> None:
    #     with self.conn:
    #         self.cursor.execute(
    #             """
    #             UPDATE user
    #               SET question_id = (?)
    #               WHERE id == (?);
    #             """,
    #             (0, user_id),
    #         )

    # def get_score(self, user_id: int) -> int:
    #     with self.conn:
    #         self.cursor.execute(
    #             """
    #             SELECT score
    #               FROM user
    #               WHERE id == (?);
    #             """,
    #             (user_id,),
    #         )
    #
    #         score: int = self.cursor.fetchone()[0]
    #
    #     return score

    def add_point(self, user_id: int) -> None:
        with self.conn:
            self.cursor.execute(
                """
                UPDATE user
                  SET score = score + 1
                  WHERE id == (?);
                """,
                (user_id,),
            )

    # def reset_user_score(self, user_id: int) -> None:
    #     with self.conn:
    #         self.cursor.execute(
    #             """
    #             UPDATE user
    #               SET score = (?)
    #               WHERE id == (?);
    #             """,
    #             (0, user_id),
    #         )

    # def get_top_10_users_results(self) -> list[tuple]:
    #     with self.conn:
    #         self.cursor.execute(
    #             """
    #             SELECT name, score
    #               FROM user
    #               ORDER BY score DESC
    #               LIMIT 10;
    #             """,
    #         )
    #
    #         results: list[tuple] = self.cursor.fetchall()
    #     return results


db = Database('database.sqlite3')
