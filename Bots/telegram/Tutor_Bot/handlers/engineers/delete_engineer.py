import asyncio
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.logger.logger import logger
from Bots.telegram.asinc_requests.asinc_requests import del_engineer
from Bots.telegram.Tutor_Bot.keyboards.main_keyboard import main_tutor_kb


router = Router()

class DelEngineer(StatesGroup):
    choosing_number = State()


@router.message(F.text.lower() == "удалить инженера")
async def add_engineer(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("Введите номер инженера которого хотите удалить:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(DelEngineer.choosing_number)



@router.message(DelEngineer.choosing_number)
async def name_chosen(message: Message, state: FSMContext):
    try:
        number = int(message.text.lower())
        await state.update_data(chosen_number=number)
        logger.info(f"user {str(message.from_user.url)} del_engineer params: number={number}")
        response = await del_engineer(number, str(message.from_user.url))

        if response:
            await message.answer(
                text=f'инженер {number} удален успешно',
                reply_markup=main_tutor_kb()
            )
        else:
            await message.answer(
                text=f'возникла ошибка при удалении инженера {number}',
                reply_markup=main_tutor_kb()
            )
        await state.clear()
    except:
        await message.answer(
            text=f'Введите номер инженера цифрами',
            reply_markup=main_tutor_kb()
        )
        await state.set_state(DelEngineer.choosing_number)

