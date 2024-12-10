""" Инициализатор бота """

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

# from bot.handlers.main_handlers import router
from signal_bot.config import bot_token
from signal_bot.bot.handlers import main_handlers, signal_handlers

bot = Bot(token=bot_token,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(main_handlers.router)
dp.include_router(signal_handlers.router)
