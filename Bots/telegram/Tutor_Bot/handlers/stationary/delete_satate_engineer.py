import asyncio
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from Bots.logger.logger import logger
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.telegram.asinc_requests.asinc_requests import del_state_engineer
from Bots.telegram.Tutor_Bot.keyboards.main_keyboard import main_tutor_kb


router = Router()

class DelStateEngineer(StatesGroup):
    choosing_number = State()


@router.message(F.text.lower() == "удалить стационарного инженера")
async def add_engineer(message: Message, state: FSMContext):
    await message.reply("Введите имя стационарного инженера которого хотите удалить:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(DelStateEngineer.choosing_number)

@router.message(DelStateEngineer.choosing_number)
async def name_chosen(message: Message, state: FSMContext):
    try:
        state_engineer_number = int(message.text.lower())
        await state.update_data(chosen_number=state_engineer_number)
        logger.info(
            f"user {str(message.from_user.url)} del_state_engineer params: state_engineers_number={state_engineer_number}")
        response = await del_state_engineer(state_engineer_number, str(message.from_user.url))
        if response:
            await message.answer(
                text=f'стационарный инженер {state_engineer_number} удален успешно',
                reply_markup=main_tutor_kb()
            )
        else:
            await message.answer(
                text=f'возникла ошибка при удалении стационарного инженера {state_engineer_number}',
                reply_markup=main_tutor_kb()
            )
    except:
        await message.answer(
            text=f'введите номер стационарного инженера цифрами пожалуйста',
        )
        await state.set_state(DelStateEngineer.choosing_number)