import asyncio
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from datetime import datetime, timedelta
from aiogram.fsm.context import FSMContext
from Bots.logger.logger import logger
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.telegram.asinc_requests.asinc_requests import get_stationary_orders_engineer, create_stationary
from Bots.telegram.Engineer_Bot.keyboards.main_keyboard import main_engineer_kb, \
    back_to_orders_engineer_kb, orders_engineer_kb, prepayment_engineer_kb, prepayment_type_engineer_kb
from dotenv import load_dotenv
import os

router = Router()


class Stationary(StatesGroup):
    choosing_photo = State()
    choosing_description = State()
    choosing_date = State()


@router.message(F.text.lower() == "стационар")
async def engineers(message: Message):
    logger.info(
        f"user {str(message.from_user.url)} get_stationary_orders_engineer")
    response = await get_stationary_orders_engineer(str(message.from_user.url))
    if response:
        message_text = "Список заказов готовых для стационара:\n\n"
        for order in response:
            order_info = f"Номер заказа: {order['order_number']} сдать в стационар -> /stationary_{order['order_number']}\n\n"
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


@router.message(lambda message: message.text and message.text.startswith('/stationary_'))
async def cmd_food(message: Message, state: FSMContext):
    command, order_number = message.text.split('_', 1)
    await state.update_data(order_number=int(order_number))

    await message.reply(text=f"пожалуйста, пришлите фото", reply_markup=back_to_orders_engineer_kb())
    await state.set_state(Stationary.choosing_photo)



@router.message(Stationary.choosing_photo)
async def name_chosen(message: Message, state: FSMContext, bot):
    if message.photo:
        photo_info = message.photo[-1]
        photo_file = await bot.get_file(photo_info.file_id)
        load_dotenv()
        token = os.environ.get("ENGINEER_BOT_TOKEN")
        photo_url = f'https://api.telegram.org/file/bot{token}/{photo_file.file_path}'
        await state.update_data(photo=photo_url)
        await message.answer(
            text="Спасибо. Теперь, пожалуйста, дату до которой надо закрыть заказ в формате: год-месяц-число",
            reply_markup=back_to_orders_engineer_kb()
        )
        await state.set_state(Stationary.choosing_date)
    else:
        await message.answer(
            text="пришлите, пожалуйта, фотографию:",
        )
        await state.set_state(Stationary.choosing_photo)

@router.message(Stationary.choosing_date)
async def engineers(message: Message, state: FSMContext):
    try:
        date_str = message.text.lower()
        penalty_date = datetime.strptime(date_str, "%Y-%m-%d") + timedelta(hours=0, minutes=0, seconds=0,
                                                                           milliseconds=0)
        date = penalty_date.isoformat() + 'Z'
        await state.update_data(date=date)
        await message.answer(
            text="теперь напишите описание:",
        )
        await state.set_state(Stationary.choosing_description)
    except:
        await message.answer(
            text="напишите дату в формате: год-месяц-число:",
        )
        await state.set_state(Stationary.choosing_date)
    # Преобразование строки в объект datetime

@router.message(Stationary.choosing_description)
async def engineers(message: Message, state: FSMContext):
    user_data = await state.get_data()
    data = {
        "order_number": user_data['order_number'],
        "photo": user_data['photo'],
        "date": user_data['date'],
        "description": message.text.lower()
    }
    logger.info(
        f"user {str(message.from_user.url)} create_stationary")
    response = await create_stationary(data, str(message.from_user.url))
    if response:
        await message.reply(text=f"заказ успешно сдан в стационар:", reply_markup=orders_engineer_kb())
    else:
        await message.reply(text=f"возникла ошибка при сдаче заказа в стационар:", reply_markup=orders_engineer_kb())
    await state.clear()


