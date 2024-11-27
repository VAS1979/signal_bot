""" Модуль содержит клавиатуры """

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# реплай стартовая клавиатура с кнопками
reply_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Создать сигнал"),
     KeyboardButton(text="Удалить сигнал")]
],
                    resize_keyboard=True,
                    input_field_placeholder="Выберите пункт меню.")
