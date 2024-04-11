import asyncio
import os
from aiogram import Router, F
from datetime import datetime
from aiogram.filters import Command, StateFilter
from aiogram.fsm import state
from Bots.logger.logger import logger
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types import FSInputFile, URLInputFile
from Bots.telegram.asinc_requests.asinc_requests import get_full_order_by_tutor, get_stages_agreement_tutor,\
    approve_agreement_tutor, delete_agreement_tutor
from Bots.telegram.Tutor_Bot.keyboards.main_keyboard import main_tutor_kb, orders_tutor_kb, stages_tutor_kb
from PIL import Image

router = Router()

@router.message(F.text.lower() == "согласование")
async def get_all_engineers(message: Message, state: FSMContext):
    await state.clear()
    logger.info(f"user {str(message.from_user.url)} get_stages_agreement_tutor")
    response = await get_stages_agreement_tutor(str(message.from_user.url))
    if response:
        # text = "согласования для подтверждения:\n\n"
        for agreement in response:
            forks = ""
            rejection = ""
            agreement_date_str = agreement['update_time'].rstrip('Z')
            agreement_date = datetime.fromisoformat(agreement_date_str)
            agreement_date_part = agreement_date.date()
            agreement_time = agreement_date.strftime("%H:%M")
            for fork in agreement["agreement_details"]["forks"]:
                forks += f"описание позиции:\n" \
                         f"описание вилки: {fork['description']}\n" \
                         f"предложенная цена: {fork['amount']}\n\n"

            if agreement["agreement_details"]["rejection"]:
                rejection += f"описание отказа: {agreement['agreement_details']['rejection']['description']}\n"

            agreement_data = f"согласование:\n" \
                             f"заказ номер: {agreement['order_number']}\n" \
                             f"дата последнего обновления: {agreement_date_part}\n" \
                             f"время последнего обновления: {agreement_time}\n" \
                             f"итоговая согласованная сумма: {agreement['amount']}\n" \
                             f"подтвердить согласование -> /approveagr_{agreement['order_number']}\n" \
                             f"удалить согласование -> /delagr_{agreement['order_number']}\n" \
                             f"Вилка цен:\n\n" + forks + rejection \


            await message.answer(
                text=agreement_data,
                reply_markup=stages_tutor_kb()
            )
    else:
        await message.answer(
            "возникли ошибки при запросе",
            reply_markup=stages_tutor_kb()
        )


@router.message(lambda message: message.text.startswith('/approveagr_'))
async def cmd_food(message: Message, state: FSMContext):
    await state.clear()
    command, order_number = message.text.split('_', 1)
    logger.info(f"user {str(message.from_user.url)} approve_agreement_tutor params: order_number={order_number}")
    response = await approve_agreement_tutor(order_number, str(message.from_user.url))
    if response:
        await message.answer(
            "согласование принято, заказ перешел на следующую стадию",
            reply_markup=stages_tutor_kb()
        )
    else:
        await message.answer(
            "возникли ошибки",
            reply_markup=stages_tutor_kb()
        )

@router.message(lambda message: message.text.startswith('/delagr_'))
async def cmd_food(message: Message, state: FSMContext):
    await state.clear()
    command, order_number = message.text.split('_', 1)
    logger.info(f"user {str(message.from_user.url)} delete_agreement_tutor params: order_number={order_number}")
    response = await delete_agreement_tutor(order_number, str(message.from_user.url))
    if response:
        await message.answer(
            "согласование удалено, инженер может заного согласовать.",
            reply_markup=stages_tutor_kb()
        )
    else:
        await message.answer(
            "возникли ошибки",
            reply_markup=stages_tutor_kb()
        )