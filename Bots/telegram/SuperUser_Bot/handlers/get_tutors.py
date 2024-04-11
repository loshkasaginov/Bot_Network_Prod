import asyncio
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from Bots.logger.logger import logger
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.telegram.asinc_requests.asinc_requests import get_tutors
from Bots.telegram.SuperUser_Bot.keyboards.main_keyboard import main_superuser_kb


router = Router()


@router.message(F.text.lower() == "посмотреть всех кураторов")
async def get_all_tutors(message: Message):
    logger.info(
        f"user {str(message.from_user.url)} get_tutors")
    response = await get_tutors(str(message.from_user.url))
    # print(response_data)
    if response:
        message_text = "Список кураторов:\n\n"
        for tutor in response:
            tutor_info = f"Номер: {tutor['tutors_number']}  " \
                         f"Имя: {tutor['name']}  " \
                         f"Ссылка: {tutor['link']}\n"
            message_text += tutor_info
        await message.answer(
            text=message_text,
            reply_markup=main_superuser_kb()
        )
    else:
        await message.answer(
            text="Ошибка доступа.",
            reply_markup=main_superuser_kb()
        )


