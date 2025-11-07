from enum import StrEnum
from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

WELCOME_MSG: str = '🤔 Привет! Готов проверить знания?'
START_MSG: str = '▶️ Начать викторину'
END_MSG: str = '👍 Вы прошли викторину!'
NEW_GAME_MSG: str = '0️⃣ Счет обнулён. Желаете сыграть еще раз?'


class EndKeyboardEnum(StrEnum):
    show_result = '🧮 Показать результат'
    show_leaderboard = '🏆 Показать таблицу рекордов'
    new_game = '🆕 Новая игра'
