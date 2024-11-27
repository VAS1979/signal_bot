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


async def write_finished_data(column_count, table_name, securities_list):
    """ Заполняет базу данных значениями из
    полученного ответа на запрос парсера """

    try:
        async with aiosqlite.connect(DB_PATH) as db_connection:
            async with db_connection.cursor() as cursor:

                insert_query = f"INSERT INTO {table_name} VALUES \
                    ({','.join(['?'] * column_count)})"

                await cursor.execute(f"DELETE FROM {table_name}")
                await db_connection.commit()

                for i in range(column_count):
                    await cursor.execute(insert_query, (securities_list[i]))
                await db_connection.commit()
                logger.info("Записи успешно добавлены в таблицу")

    except aiosqlite.Error:
        logger.error("Ошибка при подключении к базе данных")


async def write_user_signal(table_name, data_list):
    """ Записывает параметры сигналов,
    заданные пользователем """

    try:
        async with aiosqlite.connect(DB_PATH) as db_connection:
            async with db_connection.cursor() as cursor:

                insert_query = f"INSERT INTO {table_name} VALUES (?, ?, ?, ?)"

                await cursor.execute(insert_query, data_list)
                await db_connection.commit()
                logger.info("Записи успешно добавлены в таблицу, %s",
                            table_name)

    except aiosqlite.Error as m:
        logger.error("Ошибка при подключении к базе данных: %s", m)


async def make_selection_of_tickers(table_name):
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

    except aiosqlite.Error as m:
        logger.error("Ошибка при подключении к базе данных или \
выполнении запроса: %s", m)
        return None
