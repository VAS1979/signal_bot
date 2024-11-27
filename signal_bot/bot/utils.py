""" Содержит служебные функции пакета bot """

from signal_bot.config import logger
from signal_bot.repositories import make_selection_of_tickers

action_list = ["buy", "sell"]


async def check_ticker_in_database(table_name: str, ticker: str):
    """ Проверяет наличие названия
    ценной бумаги в базе данных """
    lst = await make_selection_of_tickers(table_name)

    upper_ticker = ticker.upper()
    try:
        if upper_ticker in lst:
            info = "Запрашиваемый тикер %s найден в списке"
            logger.info(info, upper_ticker)
            return upper_ticker
        else:
            find_error = "Запрашиваемый тикер %s отсутствует в списке"
            logger.info(find_error, upper_ticker)
            return

    except Exception as m:
        logger.error("Ошибка проверки данных: %s", m)


async def generate_user_signal(table_name, user_id, action, ticker, price):
    """ Создает список, формирующий сигнал
    пользователя для записи в бд """
    try:
        signal_list = []

        # добавление user_id в список
        signal_list.append(user_id)

        # добавление действия в список
        if action in action_list:
            signal_list.append(action)
        else:
            return "Некорректный сигнал"

        # проверка и добавление тикера
        result = await check_ticker_in_database(table_name, str(ticker))
        if result:
            signal_list.append(result)
        else:
            return "Веден некорректный тикер "

        # проверка и добавление цены
        if isinstance(price, (float, int)):
            signal_list.append(price)
        else:
            return "Некорректный ввод цены"

        return signal_list

    except Exception as m:
        logger.error("Ошибка проверки данных: %s", m)
