""" Модуль конфигурации парсера """

import os
import logging
from dotenv import load_dotenv

load_dotenv()

# токен бота
bot_token = os.getenv("BOT_TOKEN")

# IP адрес
URL = os.getenv("URL")

# порт подключения
PORT = int(os.getenv("PORT"))

# адрес эндпоинта для приема webhook
WEBHOOK_PATH = "/webhook"

# полный адрес для приема webhook
WEBHOOK_URL = URL + WEBHOOK_PATH

# путь к базе данных
DB_PATH = "signal_bot/db/data_db.db"

# период между опросами парсера в секундах
PERIOD_BETWEEN_REQUEST = 54

# настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# адрес запроса к MOEX по акциям
SHARE_URL = ("http://iss.moex.com/iss/engines/stock/markets/shares/boards/"
             "TQBR/securities.json?iss.meta=off")

# адрес запроса по акции SBER (для тестирования работы MOEX)
SHARE_SBER_URL = ("http://iss.moex.com/iss/engines/stock/markets/"
                  "shares/boards/TQBR/securities/SBER.json?"
                  "iss.meta=off&iss.only=marketdata&marketdata."
                  "columns=SECID,LAST")

# список типов операций
TYPE_LIST = ["buy", "sell"]

# наименование таблицы со списком ценных бумаг
TABLE_NAME = "shares"
SIGNALS = "requested_data"

# словарь приведения соответствия типов данных
CONVERT_TYPES = {
    "<class 'str'>": "TEXT",
    "<class 'float'>": "REAL",
    "<class 'int'>": "INTEGER",
    "<class 'NoneType'>": "NUMERIC"
        }

# Названия таблиц в базе данных
SHARES = "shares"
REQUESTED_DATA = "requested_data"

# Строка создания запроса к бд по созданию таблицы REQUESTED_DATA
REQUESTED_DATA_COLUMN = "DATETIME STRING, USER_ID INTEGER, SIGNAL_TYPE STRING,\
                        ASSET_NAME STRING, SIGNAL_PRICE REAL"

# Шаблон для проверки изменений типов и наименований столбцов таблицы акций
SHARES_COLUMN_TEMPLATE = [
    'SECID', 'BOARDID', 'SHORTNAME', 'PREVPRICE', 'LOTSIZE', 'FACEVALUE',
    'STATUS', 'BOARDNAME', 'DECIMALS', 'SECNAME', 'REMARKS', 'MARKETCODE',
    'INSTRID', 'SECTORID', 'MINSTEP', 'PREVWAPRICE', 'FACEUNIT', 'PREVDATE',
    'ISSUESIZE', 'ISIN', 'LATNAME', 'REGNUMBER', 'PREVLEGALCLOSEPRICE',
    'CURRENCYID', 'SECTYPE', 'LISTLEVEL', 'SETTLEDATE'
    ]

# список соответствий названий таблиц и адресов шлюзов
TYPES_SECURITIES = [[SHARES, SHARE_URL, SHARES_COLUMN_TEMPLATE]]

# список колонок во вложенном словаре json ответе MOEX
# допустимые структуры ответа:
# {"marketdata": {"columns": [], "data": []} изолированный запрос по SBER
# {"securities": {"columns": [], "data": []} запрос по всем бумагам
REQUIRED_KEYS = ["columns", "data"]

# словарь первичных ключей в json ответе MOEX
REQUEST_KEY = {"check": "marketdata", "req": "securities"}
