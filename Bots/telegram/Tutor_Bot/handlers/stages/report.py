import asyncio
import os
from aiogram import Router, F
from datetime import datetime
from aiogram.filters import Command, StateFilter
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.logger.logger import logger
from aiogram.types import FSInputFile, URLInputFile
from Bots.telegram.asinc_requests.asinc_requests import approve_report_tutor, get_stages_report_tutor, delete_report_tutor, \
    get_photo, download_photo
from Bots.telegram.Tutor_Bot.keyboards.main_keyboard import main_tutor_kb, orders_tutor_kb, stages_tutor_kb
from PIL import Image

router = Router()

class Photo(StatesGroup):
    photo = State()

@router.message(F.text.lower() == "отчет")
async def get_all_engineers(message: Message, state: FSMContext):
    await state.clear()
    logger.info(f"user {str(message.from_user.url)} get_stages_report_tutor")
    response = await get_stages_report_tutor(str(message.from_user.url))
    if response:
        # text = "согласования для подтверждения:\n\n"
        for report in response:

            report_date_str = report['update_time'].rstrip('Z')
            report_date = datetime.fromisoformat(report_date_str)
            report_date_part = report_date.date()
            report_time = report_date.strftime("%H:%M")

            report_data = f"отчет:\n" \
                          f"номер заказа: {report['order_number']}\n" \
                          f"подтвердить отчет -> /approverep_{report['order_number']}\n" \
                          f"отменить отчет -> /delrep_{report['order_number']}\n" \
                          f"общая сумма: {report['all_amount']}\n" \
                          f"сумма чистыми: {report['clear_amount']}\n" \
                          f"сумма аванса: {report['advance_payment']}\n" \
                          f"тип оплаты: {report['type_of_payment']}\n" \
                          f"дата последнего обновления: {report_date_part}\n" \
                          f"время последнего обновления: {report_time}\n"
            try:
                url = f"{report['photo_of_agreement']}"
                photo = URLInputFile(url)
                await message.answer_photo(photo, caption=report_data)
            except:
                await message.answer(
                    text=report_data,
                    reply_markup=stages_tutor_kb()
                )
    else:
        await message.answer(
            "возникли ошибки при запросе",
            reply_markup=stages_tutor_kb()
        )


@router.message(lambda message: message.text.startswith('/approverep_'))
async def cmd_food(message: Message, state: FSMContext):
    await state.clear()
    command, order_number = message.text.split('_', 1)
    logger.info(f"user {str(message.from_user.url)} approve_report_tutor params: order_number={order_number}")
    response = await approve_report_tutor(order_number, str(message.from_user.url))
    if response:
        photo =  await get_photo(order_number, str(message.from_user.url))
        if photo["photo"]:
            file_name = f"media/{order_number}.jpg"
            await download_photo(photo["photo"], file_name)
        await message.answer(
            "отчет принят. заказ окончен",
            reply_markup=stages_tutor_kb()
        )
    else:
        await message.answer(
            "возникли ошибки",
            reply_markup=stages_tutor_kb()
        )

@router.message(lambda message: message.text.startswith('/delrep_'))
async def cmd_food(message: Message, state: FSMContext):
    command, order_number = message.text.split('_', 1)
    await state.clear()
    logger.info(f"user {str(message.from_user.url)} delete_report_tutor params: order_number={order_number}")
    response = await delete_report_tutor(order_number, str(message.from_user.url))
    if response:
        await message.answer(
            "отчет удален, инженер может заного отчитаться.",
            reply_markup=stages_tutor_kb()
        )
    else:
        await message.answer(
            "возникли ошибки",
            reply_markup=stages_tutor_kb()
        )