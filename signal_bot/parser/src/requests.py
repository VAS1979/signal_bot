""" Запросы к бирже MOEX """

import aiohttp

from signal_bot.config import logger
from signal_bot.parser.src.test_response import check_response


async def request_share_sber(res: str):
    """ Запрашивает котировки SBER """

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res, timeout=5) as resp:
                content = await resp.json(content_type=None)
                await check_response(content, "check")
            share_sber_price = content["marketdata"]["data"][0][1]
#            share_sber_price = 999  # отключает проверку работы биржи
            if share_sber_price is None:
                raise ValueError("MOEX не работает\n")
            logger.info("Проверка работы биржи успешна")
            return res
    except (aiohttp.ClientError, IndexError, KeyError, TypeError,
            ValueError) as e:
        logger.error("Ошибка выполнения тестового запроса, %s", e)
        raise


async def request_securities(client, url: str):
    """ Запрос к MOEX """

    logger.info("Запрос парсера %s", url)
    try:
        async with client.get(url, timeout=5) as response:
            response.raise_for_status()
            content = await response.json(content_type=None)
        logger.info("Запрос успешно выполнен")
    except aiohttp.ClientError as e:
        logger.error("Ошибка выполнения запроса: %s", e)
        return None
    return content
