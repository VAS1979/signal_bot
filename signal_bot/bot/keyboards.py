""" Модуль содержит клавиатуры """

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# реплай стартовая клавиатура с кнопками
reply_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Создать сигнал"),
     KeyboardButton(text="Удалить сигнал"),
     KeyboardButton(text="Активные сигналы")]
],
                    resize_keyboard=True,
                    input_field_placeholder="Выберите пункт меню")

# реплай клавиатура выбора типа операции с кнопками
reply_signal_type = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="buy"),
     KeyboardButton(text="sell")]
],
                    resize_keyboard=True,
                    input_field_placeholder="Выберите тип сигнала")
