from aiogram import Router, F, types
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.telegram.Engineer_Bot.keyboards.main_keyboard import main_engineer_kb, account_engineer_kb, orders_engineer_kb, back_to_orders_engineer_kb
from aiogram.fsm.context import FSMContext


router = Router()

@router.message(F.text.lower() == "личный кабинет")
async def engineers(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("Выберите действие:", reply_markup=account_engineer_kb())

@router.message(F.text.lower() == "заказы")
async def stationary(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("Выберите действие с заказами:", reply_markup=orders_engineer_kb())

# @router.message(F.text.lower() == "заказы")
# async def orders(message: Message):
#     await message.reply("Выберите действие с заказами:", reply_markup=orders_tutor_kb())
#
@router.message(F.text.lower() == "назад")
async def back(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("выберите действие:", reply_markup=main_engineer_kb())

@router.message(F.text.lower() == "назад к заказам")
async def back(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("выберите действие:", reply_markup=orders_engineer_kb())
#
# @router.message(F.text.lower() == "инженеры")
# async def add_tutor(message: Message):
#     await message.reply("Выберите действие с инженерами:", reply_markup=main_tutor_kb())
