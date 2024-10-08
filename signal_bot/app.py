""" Точка входа в приложение """
import os
import asyncio
import logging
from contextlib import asynccontextmanager
from aiogram.types import Update
from fastapi import FastAPI
from fastapi.requests import Request
import uvicorn
from dotenv import load_dotenv

from src.utils import run_background_tasks, stop_event
from src.bot.app_bot import bot, dp
from src.api.routers import router

load_dotenv()

url = os.getenv("URL")
PORT = int(os.getenv("PORT"))
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = url + WEBHOOK_PATH

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Запуск фоновых задач """
    task = None
    try:
        task = asyncio.create_task(run_background_tasks())
        logger.info("Загрузка модели базы данных")
        await bot.set_webhook(url=WEBHOOK_URL,
                              allowed_updates=dp.resolve_used_update_types(),
                              drop_pending_updates=True)
        yield
        logger.info("Выгрузка модели базы данных")
        await bot.delete_webhook()
    finally:
        stop_event.set()
        task.cancel()
        await task


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.post(WEBHOOK_PATH)
async def webhook(request: Request) -> None:
    """ . """
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)
