import asyncio
import os
from aiogram import Router, F
from datetime import datetime
from aiogram.filters import Command, StateFilter
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from Bots.logger.logger import logger
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types import FSInputFile, URLInputFile
from Bots.telegram.asinc_requests.asinc_requests import get_full_order_by_tutor, get_stages_prepayment_tutor,\
    approve_prepayment_tutor, delete_prepayment_tutor
from Bots.telegram.Tutor_Bot.keyboards.main_keyboard import main_tutor_kb, orders_tutor_kb, stages_tutor_kb
from PIL import Image

router = Router()



@router.message(F.text.lower() == "предоплата")
async def get_all_engineers(message: Message, state: FSMContext):
    await state.clear()
    logger.info(f"user {str(message.from_user.url)} get_stages_prepayment_tutor")
    response = await get_stages_prepayment_tutor(str(message.from_user.url))
    if response:
        # text = "согласования для подтверждения:\n\n"
        for p in response:
            prepayment_date_str = p['update_time'].rstrip('Z')
            prepayment_date = datetime.fromisoformat(prepayment_date_str)
            prepayment_date_part = prepayment_date.date()
            prepayment_time = prepayment_date.strftime("%H:%M")
            prep = f"предоплата:\n" \
            f"сумма предоплаты: {p['amount']}\n" \
                   f"номер заказа: {p['order_number']}\n" \
                   f"подтвердить предоплату -> /approvepred_{p['order_number']}\n" \
                   f"удалить предоплату -> /delpred_{p['order_number']}\n" \
                   f"тип предоплаты: {p['type_of_payment']}\n" \
                         f"дата последнего обновления: {prepayment_date_part}\n" \
                         f"время последнего обновления: {prepayment_time}\n" \

            await message.answer(
                        text=prep,
                        reply_markup=stages_tutor_kb()
                    )
    else:
        await message.answer(
            "возникли ошибки при запросе",
            reply_markup=stages_tutor_kb()
        )


@router.message(lambda message: message.text.startswith('/approvepred_'))
async def cmd_food(message: Message, state: FSMContext):
    await state.clear()
    command, order_number = message.text.split('_', 1)
    logger.info(f"user {str(message.from_user.url)} approve_prepayment_tutor params: order_number={order_number}")
    response = await approve_prepayment_tutor(order_number, str(message.from_user.url))
    if response:
        await message.answer(
            "предоплата принята, заказ перешел на следующую стадию",
            reply_markup=stages_tutor_kb()
        )
    else:
        await message.answer(
            "возникли ошибки",
            reply_markup=stages_tutor_kb()
        )

@router.message(lambda message: message.text.startswith('/delpred_'))
async def cmd_food(message: Message, state: FSMContext):
    await state.clear()
    command, order_number = message.text.split('_', 1)
    logger.info(f"user {str(message.from_user.url)} delete_prepayment_tutor params: order_number={order_number}")
    response = await delete_prepayment_tutor(order_number, str(message.from_user.url))
    if response:
        await message.answer(
            "предоплата удалена, инженер может заного отчитаться по предоплате.",
            reply_markup=stages_tutor_kb()
        )
    else:
        await message.answer(
            "возникли ошибки",
            reply_markup=stages_tutor_kb()
        )