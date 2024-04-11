import asyncio
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from Bots.logger.logger import logger
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.telegram.Tutor_Bot.keyboards.main_keyboard import *
from Bots.telegram.asinc_requests.asinc_requests import get_stages_tutor

router = Router()

@router.message(F.text.lower() == "инженеры")
async def engineers(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("Выберите действие с инженерами:", reply_markup=engineers_tutor_kb())


@router.message(F.text.lower() == "заказы")
async def orders(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("Выберите действие с заказами:", reply_markup=orders_tutor_kb())

@router.message(F.text.lower() == "назад")
async def back(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("выберите действие:", reply_markup=main_tutor_kb())


@router.message(F.text.lower() == "стационар")
async def back(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("выберите действие:", reply_markup=stationary_tutor_kb())


@router.message(F.text.lower() == "стационарные инженеры")
async def back(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("выберите действие:", reply_markup=stationary_engineer_tutor_kb())


@router.message(F.text.lower() == "заказы в стационаре")
async def back(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("выберите действие:", reply_markup=stationary_orders_tutor_kb())

@router.message(F.text.lower() == "стадии")
async def back(message: Message, state: FSMContext):
    await state.clear()
    logger.info(f"user {str(message.from_user.url)} get_stages_tutor")
    response = await get_stages_tutor(str(message.from_user.url))
    if response:
        text = "количество заказов на каждой стадии готовых для проверки\n" \
               f"согласование: {response['agreements']}\n" \
               f"предоплата: {response['prepayments']}\n" \
               f"оприход: {response['outlays']}\n" \
               f"отчет: {response['reports']}\n"

        await message.reply(text=text, reply_markup=stages_tutor_kb())
    else:
        await message.reply("ошибка доступа", reply_markup=main_tutor_kb())


