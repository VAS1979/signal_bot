""" Фоновые задачи """
import asyncio
import logging

# Настройка логов
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Чтобы параллельную задачу можно было грохнуть после остановки приложения.
stop_event = asyncio.Event()


async def run_background_tasks():
    """ Запускает фоновые задачи """
    while not stop_event.is_set():
        try:
            logger.info("Фоновая задача 'Опрос MOEX по котировкам'")
            logger.info("Фоновая задача 2")
            logger.info("Фоновая задача 3")
            await asyncio.sleep(9)
        except asyncio.CancelledError:
            logger.info("Параллельная задача была остановлена.")
