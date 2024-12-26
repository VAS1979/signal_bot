""" Хэндлеры """

from aiogram import types, Router
from aiogram.filters import Command

from signal_bot.bot.keyboards import reply_main

router = Router()


@router.message(Command('start'))
async def start_handler(message: types.Message):
    """ Стартовый хэндлер """

    await message.answer(f"Привет {message.from_user.first_name},\
    {message.from_user.id}", reply_markup=reply_main)
