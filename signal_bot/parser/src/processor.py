""" Последовательно обрабатывает цепочку вызовов функций """

import aiohttp

from signal_bot.parser.src.requests import request_securities
from signal_bot.parser.src.test_response import check_response
from signal_bot.parser.src.type_column import create_column_typing
from signal_bot.repositories import (create_db_tables,
                                     write_finished_data)


async def handle_call_chain(name_table, url, template):
    """ Обрабатывает цепочки вызовов """

    async with aiohttp.ClientSession() as session:
        response = await request_securities(session, url)

    await check_response(response, "req")

    securities_list = response["securities"]["data"]

    column_create = await create_column_typing(response, template)
    await create_db_tables(column_create[0], name_table, True)
    await write_finished_data(column_create[1], name_table,
                              securities_list)
