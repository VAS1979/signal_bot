""" Хэндлеры для создания сигналов пользователя """

from mailbox import Message
from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import TABLE_NAME
from signal_bot.bot.utils import (check_operation_type,
                                  check_ticker_in_database,
                                  generate_final_result,
                                  generate_signals_report)
from signal_bot.bot.keyboards import reply_signal_type, reply_main

router = Router()


class UserSignal(StatesGroup):
    """ Класс fsm состояния
    форимрования сигнала пользователя """
    user_id = State()
    signal_type = State()
    asset_name = State()
    signal_price = State()


@router.message(F.text == "Создать сигнал")
async def select_securitie_type(message: types.Message, state: FSMContext):
    """ . """
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(UserSignal.signal_type)
    await message.answer("Выберите тип операции",
                         reply_markup=reply_signal_type)


@router.message(UserSignal.signal_type)
async def select_asset_name(message: Message, state: FSMContext):
    """ . """

    check_operation = await check_operation_type(message.text)
    if check_operation:
        await state.update_data(signal_price=message.text)
    else:
        mess = "Некорректный тип операции, введите buy или sell"
        await message.answer(text=mess)
        return

    await state.update_data(signal_type=message.text)
    await state.set_state(UserSignal.asset_name)
    reply_text = "Введите тикер"
    await message.reply(reply_text, reply_markup=types.ReplyKeyboardRemove())


@router.message(UserSignal.asset_name)
async def select_signal_price(message: Message, state: FSMContext):
    """ . """
    asset_name = message.text.upper()
    table_name = TABLE_NAME

    checked_ticker = await check_ticker_in_database(table_name, asset_name)

    if checked_ticker:
        await state.update_data(asset_name=asset_name)
        await state.set_state(UserSignal.signal_price)
        await message.answer("Введите цену")
    else:
        await message.reply('Пожалуйста, введите корректный тикер')
        return


@router.message(UserSignal.signal_price, F.text)
async def complete_signal_create(message: Message, state: FSMContext):
    """ . """
    if message.text.isnumeric():
        await state.update_data(signal_price=message.text)
    else:
        await message.answer(text="Необходимо ввести число")
        return

    data = await state.get_data()
    user_id = data["user_id"]
    action = data["signal_type"]
    entered_ticker = data["asset_name"]
    entered_price = data["signal_price"]

    finish_massage = await generate_final_result(user_id, action,
                                                 entered_ticker, entered_price)
    await message.answer(finish_massage)
    await state.clear()


@router.message(F.text == "Активные сигналы")
async def signals_report(message: types.Message):
    """ . """
    user_id = message.from_user.id
    print(user_id)
    mess = await generate_signals_report("requested_data", user_id)
    print(mess)
    await message.answer(mess)
    await message.answer("Выберите пункт меню",
                         reply_markup=reply_main)
