""" Содержит служебные функции пакета bot """

from datetime import datetime

from signal_bot.config import (REQUESTED_DATA, REQUESTED_DATA_COLUMN,
                               TYPE_LIST, logger)
from signal_bot.repositories import (create_db_tables, delete_string_db,
                                     get_user_signal, write_user_signal,
                                     make_selection_of_tickers)


async def get_datetime():
    """ Запрашивает текущую дату и время """
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_datetime


async def check_operation_type(operation):
    """ . """
    if operation in TYPE_LIST:
        return operation
    else:
        return None


async def check_ticker_in_database(table_name: str, ticker: str):
    """ Проверяет наличие названия
    ценной бумаги в базе данных """
    lst = await make_selection_of_tickers(table_name)

    try:
        if ticker in lst:
            info = "Запрашиваемый тикер %s найден в списке"
            logger.info(info, ticker)
            return ticker
        else:
            find_error = "Запрашиваемый тикер %s отсутствует в списке"
            logger.info(find_error, ticker)
            return

    except Exception as m:
        logger.error("Ошибка проверки данных: %s", m)


async def generate_user_signal(user_id, action, ticker, price):
    """ Создает список, формирующий сигнал
    пользователя для записи в бд """
    signal_list = []

    # добавляет дату и время
    date = await get_datetime()
    signal_list.append(date)

    # добавляет user_id в список
    signal_list.append(user_id)

    # добавляет действия в список
    signal_list.append(action)

    # добавляет тикер в список
    signal_list.append(ticker)

    # добавляет цену
    signal_list.append(price)

    return signal_list


async def generate_final_result(user_id, action, ticker, price):
    """ . """
    # формирует список сигнала пользователя
    result = await generate_user_signal(user_id, action, ticker, price)
    # создает таблицу бд
    await create_db_tables(REQUESTED_DATA_COLUMN, REQUESTED_DATA)
    # сохраняет сигнал в бд
    await write_user_signal(REQUESTED_DATA, result)
    # формирует сообщение пользователю
    mes1 = f'Сигнал сформирован.\nВаш id: {user_id}\n'
    mes2 = f'Тип сигнала: {action}\n'
    mes3 = f'Тикер: {ticker}\nЦена: {price}'
    message = mes1 + mes2 + mes3

    return message


async def generate_signals_report(table_name, user_id):
    """ . """
    signal_list = await get_user_signal(table_name, user_id)

    if len(signal_list) == 0:
        return "Список сигналов пуст"

    user_message = ""
    for signal in signal_list:
        data = f"Дата создания: {signal[0]}"
        operation = f"Тип операции: {signal[2]}"
        ticker = f"Тикер: {signal[3]}"
        price = f"Цена: {str(signal[4])}"
        mess = data + "\n" + operation + "\n" + ticker + "\n" + price + "\n\n"
        user_message += mess

    return user_message


async def delete_signal(table, user_id, operation, ticker):
    """ Удаляет строки с сигналами с заданными
    параметрами при их наличии """

    del_signal = await delete_string_db(table, user_id, operation, ticker)

    if del_signal:
        return del_signal
    else:
        return "Нет сигналов с заданными параметрами"
