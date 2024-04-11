import asyncio
from datetime import datetime
from Bots.logger.logger import logger
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types import FSInputFile, URLInputFile
from Bots.telegram.asinc_requests.asinc_requests import get_all_stationary_orders_state_engineer, put_current_stationary_by_state_engineer, \
    get_personal_stationary_orders_state_engineer, end_current_stationary_by_state_engineer
from Bots.telegram.State_Engineer_Bot.keyboards.main_keyboard import main_state_engineer_kb, state_engineer_kb

router = Router()

@router.message(F.text.lower() == "посмотреть доступные заказы")
async def engineers(message: Message):
    logger.info(
        f"user {str(message.from_user.url)} get_all_stationary_orders_state_engineer")
    response = await get_all_stationary_orders_state_engineer(str(message.from_user.url))
    if response:
        message_text = "Список заказов для стационара:\n\n"
        await message.answer(
            text=message_text,
            reply_markup=state_engineer_kb(),
        )
        for stationary in response:
            sate_date_str = stationary['date'].rstrip('Z')
            state_date = datetime.fromisoformat(sate_date_str)
            state_date_part = state_date.date()
            order_info = f"Номер заказа: {stationary['order_number']}\n" \
                         f"имя инженера: {stationary['name']}\n" \
                         f"описание: {stationary['description']}\n" \
                         f"приоритет: {stationary['priority']}\n" \
                         f"выполнить до: {state_date_part}\n" \
                         f"взять заказ -> /takestate_{stationary['order_number']}\n\n"
            try:
                url = f"{stationary['photo']}"
                photo = URLInputFile(url)
                await message.answer_photo(photo, caption=order_info)
            except:
                await message.answer(
                    text=order_info,
                    reply_markup=state_engineer_kb()
                )
    else:
        await message.answer(
            text="Нет активных заказов на этой стадии, или ошибка доступа.",
            reply_markup=state_engineer_kb()
        )


@router.message(lambda message: message.text.startswith('/takestate_'))
async def cmd_food(message: Message, state: FSMContext, bot):
    command, order_number = message.text.split('_', 1)
    logger.info(
        f"user {str(message.from_user.url)} put_current_stationary_by_state_engineer")
    response = await put_current_stationary_by_state_engineer(order_number, str(message.from_user.url))
    if response:
        await message.answer(
            text="заказ успешно назначен.",
            reply_markup=state_engineer_kb()
        )
    else:
        await message.answer(
            text="произошла ошибка доступа.",
            reply_markup=state_engineer_kb()
        )

@router.message(F.text.lower() == "посмотреть личные заказы")
async def engineers(message: Message):
    logger.info(
        f"user {str(message.from_user.url)} get_personal_stationary_orders_state_engineer")
    response = await get_personal_stationary_orders_state_engineer(str(message.from_user.url))
    if response:
        message_text = "Список личных заказов:\n\n"
        await message.answer(
            text=message_text,
            reply_markup=state_engineer_kb(),
        )
        for stationary in response:
            sate_date_str = stationary['date'].rstrip('Z')
            state_date = datetime.fromisoformat(sate_date_str)
            state_date_part = state_date.date()
            order_info = f"Номер заказа: {stationary['order_number']}\n" \
                         f"имя инженера: {stationary['name']}\n" \
                         f"описание: {stationary['description']}\n" \
                         f"приоритет: {stationary['priority']}\n" \
                         f"выполнить до: {state_date_part}\n" \
                         f"отчитать заказ -> /reportorder_{stationary['order_number']}\n\n"
            try:
                url = f"{stationary['photo']}"
                photo = URLInputFile(url)
                await message.answer_photo(photo, caption=order_info)
            except:
                await message.answer(
                    text=order_info,
                    reply_markup=state_engineer_kb()
                )
    else:
        await message.answer(
            text="Нет активных заказов на этой стадии, или ошибка доступа.",
            reply_markup=state_engineer_kb()
        )

class StationaryReport(StatesGroup):
    choosing_amount = State()


@router.message(lambda message: message.text.startswith('/reportorder_'))
async def cmd_food(message: Message, state: FSMContext, bot):
    command, order_number = message.text.split('_', 1)
    await state.update_data(order_number=int(order_number))
    await message.reply(text=f"введите сумму работ", reply_markup=state_engineer_kb())
    await state.set_state(StationaryReport.choosing_amount)

@router.message(StationaryReport.choosing_amount)
async def engineers(message: Message, state: FSMContext):
    try:
        amount = int(message.text.lower())
    except:
        await message.answer(
            text="введите, пожалуйста, цифрами:",
        )
        await state.set_state(StationaryReport.choosing_amount)
    await state.update_data(amount=amount)
    user_data = await state.get_data()
    data = {
        "order_number": user_data['order_number'],
        "amount": user_data['amount'],
    }
    logger.info(
        f"user {str(message.from_user.url)} end_current_stationary_by_state_engineer")
    response = await end_current_stationary_by_state_engineer(data, str(message.from_user.url))
    if response:
        await message.reply(text=f"отчет по предоплате успешно создан:", reply_markup=state_engineer_kb())
    else:
        await message.reply(text=f"возникла ошибка при отчитывании:", reply_markup=state_engineer_kb())
    await state.clear()
