## Описание
- Этот проект разрабатывается для автоматизации торговли и помощи в выборе финансовых инструментов

## Функционал
- Парсер циклично опрашивает MOEX и раскладывает информацию в базу данных, постоянно обновляя ее
- 

## Как пользоваться
 - Установите `poetry`
 - Перейдите в консоли в папку с проектом
 - Введите команду `poetry install` для инициализации виртуального окружения и установки всех зависимостей
 - Перейдите в папку проекта `signal_bot`, где находится файл `app.py`
 - Создайте файл `.env`, скопируйте и заполните параметрами константы из файла `example.env`
 - Введите команду `poetry run python app.py`
