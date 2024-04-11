import asyncio
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from Bots.logger.logger import logger
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.telegram.asinc_requests.asinc_requests import del_tutor
from Bots.telegram.SuperUser_Bot.keyboards.main_keyboard import main_superuser_kb


router = Router()

class DelTutor(StatesGroup):
    choosing_name = State()


@router.message(F.text.lower() == "удалить куратора")
async def add_tutor(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("Введите имя куратора которого хотите удалить:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(DelTutor.choosing_name)

@router.message(DelTutor.choosing_name)
async def name_chosen(message: Message, state: FSMContext):

    name = message.text.lower()
    await state.update_data(chosen_number=name)
    logger.info(
        f"user {str(message.from_user.url)} del_tutor")
    response = await del_tutor(name, str(message.from_user.url))

    if response:
        await message.answer(
            text=f'куратор {name} удален успешно',
            reply_markup=main_superuser_kb()
        )
    else:
        await message.answer(
            text=f'возникла ошибка при удалении куратора {name}',
            reply_markup=main_superuser_kb()
        )
