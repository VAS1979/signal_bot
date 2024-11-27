""" Хэндлеры """

from aiogram import F, types, Router
from aiogram.filters import Command

from signal_bot.repositories import create_db_tables, write_user_signal
from signal_bot.config import REQUESTED_DATA, REQUESTED_DATA_COLUMN
from signal_bot.bot.keyboards import reply_main
from signal_bot.bot.utils import generate_user_signal

router = Router()


@router.message(Command('start'))
async def start_handler(message: types.Message):
    """ Стартовое приветствие """
    await message.answer(f"Привет {message.from_user.first_name},\
    {message.from_user.id}", reply_markup=reply_main)


@router.message(F.text == "Создать сигнал")
async def create_signal(message: types.Message):
    """ Создает сигнал для открытия или закрытия
    позиции и записывает его в базу данных """

    table_name = "shares"
    user_id = message.from_user.id
    action = "sell"
    entered_ticker = "aQua"
    entered_price = 999

    result = await generate_user_signal(table_name, user_id, action,
                                        entered_ticker, entered_price)

    if isinstance(result, list):
        # создает таблицу бд
        await create_db_tables(REQUESTED_DATA_COLUMN, REQUESTED_DATA)
        # сохраняет сигнал в бд и сообщает пользователю
        await write_user_signal(REQUESTED_DATA, result)
        mess = "Сигнал добавлен"
        await message.answer(mess)
    else:
        # сообщает пользователю о ошибке
        await message.answer(result)
