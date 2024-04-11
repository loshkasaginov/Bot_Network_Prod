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
from Bots.telegram.asinc_requests.asinc_requests import get_stages_outlay_tutor, approve_outlay_tutor, delete_outlays_tutor
from Bots.telegram.Tutor_Bot.keyboards.main_keyboard import main_tutor_kb, orders_tutor_kb, stages_tutor_kb
from PIL import Image

router = Router()


@router.message(F.text.lower() == "оприход")
async def get_all_engineers(message: Message, state: FSMContext):
    await state.clear()
    logger.info(f"user {str(message.from_user.url)} get_stages_outlay_tutor")
    response = await get_stages_outlay_tutor(str(message.from_user.url))
    if response:
        # text = "согласования для подтверждения:\n\n"
        for o in response:
            text = f"оприход:\n" \
                  f"номер заказа: {o['order_number']}\n" \
                  f"подтвердить оприход -> /approveoutlay_{o['order_number']}\n" \
                 f"отменить оприход -> /deloutlay_{o['order_number']}\n"
            await message.answer(
                text=text,
                reply_markup=stages_tutor_kb()
            )
            for outlay in o["outlays"]:
                outlay_date_str = outlay['update_time'].rstrip('Z')
                outlay_date = datetime.fromisoformat(outlay_date_str)
                outlay_date_part = outlay_date.date()
                outlay_time = outlay_date.strftime("%H:%M")
                outlay_data = f"номер заказа: {o['order_number']}\n" \
                              f"название оприхода: {outlay['name']}\n" \
                              f"сумма оприхода: {outlay['amount']}\n" \
                              f"тип оприхода: {outlay['type_of_payment']}\n" \
                              f"дата последнего обновления: {outlay_date_part}\n" \
                              f"время последнего обновления: {outlay_time}\n" \
                # with Image.open("photo.jpg") as im:
            #     im.show()
                try:
                    url = f"{outlay['cheque']}"
                    photo = URLInputFile(url)
                    await message.answer_photo(photo, caption=outlay_data)
                except:
                    await message.answer(
                        text=outlay_data,
                        reply_markup=stages_tutor_kb()
                    )
    else:
        await message.answer(
            "возникли ошибки при запросе",
            reply_markup=stages_tutor_kb()
        )


@router.message(lambda message: message.text.startswith('/approveoutlay_'))
async def cmd_food(message: Message, state: FSMContext):
    await state.clear()
    command, order_number = message.text.split('_', 1)
    logger.info(f"user {str(message.from_user.url)} approve_outlay_tutor params: order_number={order_number}")
    response = await approve_outlay_tutor(order_number, str(message.from_user.url))
    if response:
        await message.answer(
            "оприход принят, заказ перешел на следующую стадию",
            reply_markup=stages_tutor_kb()
        )
    else:
        await message.answer(
            "возникли ошибки",
            reply_markup=stages_tutor_kb()
        )


@router.message(lambda message: message.text.startswith('/deloutlay_'))
async def cmd_food(message: Message, state: FSMContext):
    await state.clear()
    command, order_number = message.text.split('_', 1)
    logger.info(f"user {str(message.from_user.url)} delete_outlays_tutor params: order_number={order_number}")
    response = await delete_outlays_tutor(order_number, str(message.from_user.url))
    if response:
        await message.answer(
            "оприход удале, инженер может заного отчитаться по оприходу.",
            reply_markup=stages_tutor_kb()
        )
    else:
        await message.answer(
            "возникли ошибки",
            reply_markup=stages_tutor_kb()
        )