""" Точка входа в приложение """

import asyncio
from contextlib import asynccontextmanager
from aiogram.types import Update
from fastapi import FastAPI
from fastapi.requests import Request
import uvicorn

from signal_bot.start_program_cycle import run_background_tasks, stop_event
from signal_bot.bot.app_bot import bot, dp
from signal_bot.api.routers import router
from signal_bot.config import logger, PORT, WEBHOOK_URL, WEBHOOK_PATH


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Запускает фоновы задачи """

    task = None
    try:
        logger.info("Запуск цикла сопрограмм\n")
        task = asyncio.create_task(run_background_tasks())

        await bot.set_webhook(url=WEBHOOK_URL,
                              allowed_updates=dp.resolve_used_update_types(),
                              drop_pending_updates=True)
        yield
        await bot.delete_webhook()
    finally:
        stop_event.set()
        task.cancel()
        await task
        await bot.session.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.post(WEBHOOK_PATH)
async def webhook(request: Request) -> None:
    """ Перенаправляет запросы с API телеграм бота """

    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)
