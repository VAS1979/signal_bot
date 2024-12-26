""" Фоновые задачи """
import asyncio

from repositories import create_db_tables
from signal_bot.parser.parser_core import start_parsing
from signal_bot.config import REQUESTED_DATA, REQUESTED_DATA_COLUMN, logger

# Чтобы параллельную задачу можно было грохнуть после остановки приложения.
stop_event = asyncio.Event()


async def run_background_tasks():
    """ Запускает фоновые задачи """

    # создает таблицу бд
    await create_db_tables(REQUESTED_DATA_COLUMN, REQUESTED_DATA)

    while not stop_event.is_set():
        try:
            await start_parsing()
            logger.info("Фоновая задача 2")
            logger.info("Фоновая задача 3")
            await asyncio.sleep(9)
        except asyncio.CancelledError:
            logger.info("Параллельная задача была остановлена.")
