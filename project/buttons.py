from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

_button_start_quiz = KeyboardButton('Начать викторину')
start_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(_button_start_quiz)

_button_result = KeyboardButton('Показать результат')
_button_table_records = KeyboardButton('Показать таблицу рекордов')
_button_reset_score = KeyboardButton('Сыграть заново')

end_menu = (
    ReplyKeyboardMarkup(resize_keyboard=True)
    .add(_button_result)
    .add(_button_table_records)
    .add(_button_reset_score)
)
