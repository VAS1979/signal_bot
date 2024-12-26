""" Запросы к базе данных """

import aiosqlite

from config import logger, DB_PATH


async def create_db_tables(column_create: str, table_name: str,
                           can_be_recreated=False):
    """ Создает базу, если ее нет, создает таблицу
    если ее нет, пересоздает если уже имеются """

    create_table = f"CREATE TABLE IF NOT EXISTS \
        {table_name} ({column_create})"
    try:
        async with aiosqlite.connect(DB_PATH) as db_connection:
            async with db_connection.cursor() as cursor:
                logger.info("Соединение для создания %s открыто", table_name)

                # Удаляет существующую таблицу если ее можно удалять
                if can_be_recreated is not False:
                    await cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                    await db_connection.commit()

                # Создает новую таблицу если ее нет
                await cursor.execute(create_table)
                await db_connection.commit()
                logger.info("Соединение для создания %s закрыто", table_name)
                logger.info("Таблица %s успешно обновлена.", table_name)
    except aiosqlite.Error as e:
        logger.error("Ошибка при создании/обновлении таблицы: %s", e)
    return None


async def write_finished_data(column_count, string_count, table_name,
                              securities_list):
    """ Заполняет базу данных значениями из
    полученного ответа на запрос парсера """

    try:
        async with aiosqlite.connect(DB_PATH) as db_connection:
            async with db_connection.cursor() as cursor:

                insert_query = f"INSERT INTO {table_name} VALUES \
                ({','.join(['?'] * column_count)})"

                await cursor.execute(f"DELETE FROM {table_name}")
                await db_connection.commit()

                for i in range(string_count):
                    await cursor.execute(insert_query, (securities_list[i]))
                await db_connection.commit()
                logger.info("Записи успешно добавлены в таблицу")

    except aiosqlite.Error as e:
        logger.error("Ошибка при подключении к базе данных, %s", e)


async def write_user_signal(table_name: str, data_list):
    """ Записывает параметры сигналов,
    заданные пользователем """

    try:
        async with aiosqlite.connect(DB_PATH) as db_connection:
            async with db_connection.cursor() as cursor:

                column_count = len(data_list)

                insert_query = f"INSERT INTO {table_name} VALUES \
                ({','.join(['?'] * column_count)})"

                await cursor.execute(insert_query, data_list)
                await db_connection.commit()
                logger.info("Записи успешно добавлены в таблицу, %s",
                            table_name)

    except aiosqlite.Error as e:
        logger.error("Ошибка при подключении к базе данных: %s", e)


async def make_selection_of_tickers(table_name: str):
    """ Собирает в список наименования ценных бумаг из таблицы базы данных """

    tickers = []

    try:
        async with aiosqlite.connect(DB_PATH) as db_connection:
            async with db_connection.cursor() as cursor:

                select_query = f"SELECT SECID FROM {table_name}"

                await cursor.execute(select_query)
                rows = await cursor.fetchall()
                await db_connection.commit()

                for row in rows:
                    tickers.append(row[0])

                logger.info("Записи успешно считаны из таблицы %s.\
Количество тикеров: %s", table_name, len(tickers))
                return tickers

    except aiosqlite.Error as e:
        logger.error("Ошибка при подключении к базе данных или \
выполнении запроса: %s", e)
        return None


async def get_user_signal(table_name: str, user_id: int):
    """ Делает выборку сигналов пользователя
    и формирует словарь с вложенными списками """

    signals = []

    try:
        async with aiosqlite.connect(DB_PATH) as db_connection:
            async with db_connection.cursor() as cursor:

                select_query = f"SELECT * FROM {table_name} \
                    WHERE USER_ID = {user_id}"

                await cursor.execute(select_query)
                rows = await cursor.fetchall()
                await db_connection.commit()

                for row in rows:
                    signals.append(row)

                logger.info("Записи успешно считаны из таблицы %s.\
Количество тикеров: %s", table_name, len(signals))
                return signals

    except aiosqlite.Error as e:
        logger.error("Ошибка при подключении к базе данных или \
выполнении запроса: %s", e)
        return None


async def delete_string_db(table: str, user_id: int, operation: str,
                           ticker: str):
    """ Удаляет строки с сигналами пользователя """

    try:
        async with aiosqlite.connect(DB_PATH) as db_connection:
            async with db_connection.cursor() as cursor:

                delete_query = f"DELETE FROM {table} WHERE USER_ID = ?\
                    AND SIGNAL_TYPE = ? AND ASSET_NAME = ?"

                await cursor.execute(delete_query, (user_id, operation,
                                                    ticker))
                await db_connection.commit()

                rows_affected = cursor.rowcount

                if rows_affected > 0:
                    logger.info("Успешно удалено %s строк.", rows_affected)
                    return f"Успешно удалено {rows_affected} строк."
                else:
                    return None

    except aiosqlite.Error as e:
        logger.error("Ошибка при подключении к базе данных или \
выполнении запроса(удаление строки с сигналами пользователя): %s", e)
        return None
