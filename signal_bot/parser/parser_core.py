""" Создание и заполнение базы данных """

import asyncio
import aiosqlite
import aiohttp

from signal_bot.config import (PERIOD_BETWEEN_REQUEST, logger,
                               SHARE_SBER_URL, TYPES_SECURITIES)
from signal_bot.parser.src.requests import request_share_sber
from signal_bot.parser.src.processor import handle_call_chain

# Остановка приложения через Ctrl+C
stop_event = asyncio.Event()


async def start_parsing():
    """Обрабатывает цикл вызовов
    обработчика запросов """

    try:
        await request_share_sber(SHARE_SBER_URL)
    except (aiohttp.ClientError, IndexError, KeyError,
            TypeError, ValueError, aiosqlite.Error) as m:
        logger.error("Ошибка запроса тестовой цены, %s", m)
    else:
        for name_table, url, template in TYPES_SECURITIES:
            try:
                await handle_call_chain(name_table, url, template)
            except (aiohttp.ClientError, IndexError, KeyError,
                    TypeError, ValueError, aiosqlite.Error,
                    AttributeError) as e:
                logger.error("Ошибка выполнения процесса, %s", e)
            finally:
                logger.info("Цикл обработки запроса и записи в БД завершен\n")

    await asyncio.sleep(PERIOD_BETWEEN_REQUEST)
