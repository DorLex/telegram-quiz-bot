from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# ---------Start Menu--------------
button_start_quiz = KeyboardButton('Начать викторину')
start_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(button_start_quiz)

# ---------End menu----------------
button_result = KeyboardButton('Показать результат')
button_table_records = KeyboardButton('Показать таблицу рекордов')
button_reset_score = KeyboardButton('Сыграть заново')

end_menu = (ReplyKeyboardMarkup(resize_keyboard=True).add(button_result)
            .add(button_table_records).add(button_reset_score))
