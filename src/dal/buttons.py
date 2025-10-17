from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button1: KeyboardButton = KeyboardButton(text='Начать викторину')

kb = [
    [button1],
]

start_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
    input_field_placeholder='Выберите вариант:',  # подсказка в поле ввода
)
