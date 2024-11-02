""" Инициализатор бота """
import os
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from .handlers import router

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

bot = Bot(token=bot_token,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(router)
