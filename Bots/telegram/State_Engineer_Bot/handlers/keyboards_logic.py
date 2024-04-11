from aiogram import Router, F, types
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.telegram.State_Engineer_Bot.keyboards.main_keyboard import state_engineer_kb, main_state_engineer_kb

router = Router()



@router.message(F.text.lower() == "заказы")
async def stationary(message: Message):
    await message.reply("Выберите действие с заказами:", reply_markup=state_engineer_kb())


@router.message(F.text.lower() == "назад")
async def back(message: Message):
    await message.reply("выберите действие:", reply_markup=main_state_engineer_kb())