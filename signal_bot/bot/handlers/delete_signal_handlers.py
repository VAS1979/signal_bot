""" Хэндлеры для удаления сигналов пользователя """

from mailbox import Message
from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import TABLE_NAME, SIGNALS
from signal_bot.bot.utils import (check_operation_type,
                                  check_ticker_in_database, delete_signal)
from signal_bot.bot.keyboards import reply_signal_type, reply_main

router = Router()


class DeleteUserSignal(StatesGroup):
    """ Класс fsm состояния форимрования
    удаления сигнала пользователя """
    d_user_id = State()
    d_signal_type = State()
    d_asset_name = State()


@router.message(F.text == "Удалить сигнал")
async def select_del_securitie_type(message: types.Message, state: FSMContext):
    """ . """
    await state.update_data(d_user_id=message.from_user.id)
    await state.set_state(DeleteUserSignal.d_signal_type)
    await message.answer("Выберите тип операции",
                         reply_markup=reply_signal_type)


@router.message(DeleteUserSignal.d_signal_type)
async def select_del_asset_name(message: Message, state: FSMContext):
    """ . """
    check_operation = await check_operation_type(message.text)
    if check_operation:
        await state.update_data(d_signal_type=message.text)
        await state.set_state(DeleteUserSignal.d_asset_name)
        reply_text = "Введите тикер"
    else:
        mess = "Некорректный тип операции, введите buy или sell"
        await message.answer(text=mess)
        return
    await message.reply(reply_text, reply_markup=types.ReplyKeyboardRemove())


@router.message(DeleteUserSignal.d_asset_name)
async def select_del_signal_price(message: Message, state: FSMContext):
    """ . """
    asset_name = message.text.upper()
    table_name = TABLE_NAME

    checked_ticker = await check_ticker_in_database(table_name, asset_name)

    data = await state.get_data()
    d_user_id = data["d_user_id"]
    d_action = data["d_signal_type"]

    if checked_ticker:
        await state.update_data(d_asset_name=asset_name)
        data = await state.get_data()
        mess = await delete_signal(SIGNALS, d_user_id, d_action,
                                   asset_name)
        await message.answer(mess)
        await state.clear()
        await message.answer("Выберите пункт меню",
                             reply_markup=reply_main)
    else:
        await message.reply("Строки с заданными параметрами не найдены")
        await message.answer("Выберите пункт меню",
                             reply_markup=reply_main)
