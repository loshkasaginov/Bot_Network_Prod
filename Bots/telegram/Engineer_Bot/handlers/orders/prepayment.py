import asyncio
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from Bots.logger.logger import logger
from Bots.telegram.asinc_requests.asinc_requests import get_prepayment_orders_engineer, create_prepayment
from Bots.telegram.Engineer_Bot.keyboards.main_keyboard import main_engineer_kb, \
    back_to_orders_engineer_kb, orders_engineer_kb, prepayment_engineer_kb, prepayment_type_engineer_kb


router = Router()


class Prepayment(StatesGroup):
    choosing_amount = State()
    choosing_tp_of_pmt = State()
    choosing_way = State()


@router.message(F.text.lower() == "предоплата")
async def engineers(message: Message):
    logger.info(
        f"user {str(message.from_user.url)} get_prepayment_orders_engineer")
    response = await get_prepayment_orders_engineer(str(message.from_user.url))
    if response:
        message_text = "Список заказов готовых для предоплаты:\n\n"
        for order in response:
            order_info = f"Номер заказа: {order['order_number']} отчитать по предоплате -> /makeprepayment_{order['order_number']}\n\n"
            message_text += order_info
        await message.answer(
            text=message_text,
            reply_markup=back_to_orders_engineer_kb(),
        )
    else:
        await message.answer(
            text="Нет активных заказов на этой стадии, или ошибка доступа.",
            reply_markup=orders_engineer_kb()
        )


@router.message(lambda message: message.text and message.text.startswith('/makeprepayment_'))
async def cmd_food(message: Message, state: FSMContext):
    command, order_number = message.text.split('_', 1)
    await state.update_data(order_number=int(order_number))

    await message.reply(text=f"предоплата была?", reply_markup=prepayment_engineer_kb())
    await state.set_state(Prepayment.choosing_way)

@router.message(Prepayment.choosing_way,F.text.lower() == "да")
async def engineers(message: Message, state: FSMContext):
    await message.reply(text=f"введите сумму предоплаты:",reply_markup=back_to_orders_engineer_kb())
    await state.set_state(Prepayment.choosing_amount)


@router.message(Prepayment.choosing_amount)
async def engineers(message: Message, state: FSMContext):
    try:
        amount = int(message.text.lower())
    except:
        await message.answer(
            text="введите, пожалуйста, цифрами:",
        )
        await state.set_state(Prepayment.choosing_amount)
    await state.update_data(amount=amount)
    await message.answer(
        text="теперь выберите вид предоплаты:",
        reply_markup = prepayment_type_engineer_kb()
    )
    await state.set_state(Prepayment.choosing_tp_of_pmt)


@router.message(Prepayment.choosing_way,F.text.lower() == "нет")
async def engineers(message: Message, state: FSMContext):
    user_data = await state.get_data()
    data={
        "order_number": user_data['order_number'],
        "amount": 0,
        "tp_of_pmt_id":1
    }
    response = await create_prepayment(data, str(message.from_user.url))
    if response:
        await message.reply(text=f"отчет по предоплате успешно создан:", reply_markup=orders_engineer_kb())
    else:
        await message.reply(text=f"возникла ошибка при отчитывании:", reply_markup=orders_engineer_kb())
    await state.clear()

@router.message(Prepayment.choosing_tp_of_pmt,F.text.lower() == "наличные")
async def engineers(message: Message, state: FSMContext):
    user_data = await state.get_data()
    data={
        "order_number": user_data['order_number'],
        "amount": user_data['amount'],
        "tp_of_pmt_id":2
    }
    response = await create_prepayment(data, str(message.from_user.url))
    if response:
        await message.reply(text=f"отчет по предоплате успешно создан:", reply_markup=orders_engineer_kb())
    else:
        await message.reply(text=f"возникла ошибка при отчитывании:", reply_markup=orders_engineer_kb())
    await state.clear()

@router.message(Prepayment.choosing_tp_of_pmt,F.text.lower() == "безнал")
async def engineers(message: Message, state: FSMContext):

    user_data = await state.get_data()
    data={
        "order_number": user_data['order_number'],
        "amount": user_data['amount'],
        "tp_of_pmt_id":3
    }
    logger.info(
        f"user {str(message.from_user.url)} create_prepayment")
    response = await create_prepayment(data, str(message.from_user.url))
    if response:
        await message.reply(text=f"отчет по предоплате успешно создан:", reply_markup=orders_engineer_kb())
    else:
        await message.reply(text=f"возникла ошибка при отчитывании:", reply_markup=orders_engineer_kb())
    await state.clear()