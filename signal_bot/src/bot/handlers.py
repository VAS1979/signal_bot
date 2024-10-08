""" Хэндлеры """

from aiogram import types, Router
from aiogram.filters import Command

router = Router()


@router.message(Command('start'))
async def start_handler(message: types.Message):
    """ . """
    await message.answer(f"Привет {message.from_user.first_name},\
                          {message.from_user.id}")


async def start_service_notification(message: types.Message):
    """ . """
    await message.answer("Сервер запущен")
