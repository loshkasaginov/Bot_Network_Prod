
import asyncio
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from Bots.logger.logger import logger
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.telegram.asinc_requests.asinc_requests import get_state_engineers
from Bots.telegram.Tutor_Bot.keyboards.main_keyboard import main_tutor_kb, stationary_engineer_tutor_kb


router = Router()


@router.message(F.text.lower() == "посмотреть всех стационарных инженеров")
async def get_all_state_engineers(message: Message):
    logger.info(f"user {str(message.from_user.url)} get_state_engineers")
    response = await get_state_engineers(str(message.from_user.url))
    # print(response_data)
    if response:
        message_text = "Список стационарных инженеров:\n\n"
        for engineer in response:
            engineer_info = f"Номер: {engineer['state_engineers_number']}  " \
                         f"Имя: {engineer['name']}  " \
                         f"Ссылка: {engineer['link']}\n" \
                         f"посмотреть подробнее -> /getstateengineer_{engineer['state_engineers_number']}\n\n"
            message_text += engineer_info
        await message.answer(
            text=message_text,
            reply_markup=stationary_engineer_tutor_kb()
        )
    else:
        await message.answer(
            text="Ошибка доступа.",
            reply_markup=stationary_engineer_tutor_kb()
        )





