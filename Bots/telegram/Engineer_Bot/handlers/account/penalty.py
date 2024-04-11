import asyncio
from aiogram import Router, F
from datetime import datetime
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from Bots.logger.logger import logger
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.telegram.asinc_requests.asinc_requests import get_penalty_engineer
from Bots.telegram.Engineer_Bot.keyboards.main_keyboard import main_engineer_kb

router = Router()


@router.message(F.text.lower() == "штрафы")
async def engineers(message: Message, state: FSMContext):
    await state.clear()
    logger.info(
        f"user {str(message.from_user.url)} get_penalty_engineer")
    response = await get_penalty_engineer(str(message.from_user.url))
    if response:
        text = "штрафы:\n\n"
        for penalty in response:
            penalty_date_str = penalty['update_time'].rstrip('Z')
            penalty_date = datetime.fromisoformat(penalty_date_str)
            penalty_date_part = penalty_date.date()
            penalty_time = penalty_date.strftime("%H:%M")

            text += f"сумма штрафа: {penalty['amount']}\n" \
                    f"описание: {penalty['description']}\n" \
                    f"дата добавления: {penalty_date_part}\n" \
                    f"время добавления: {penalty_time}\n\n"
        await message.answer(
            text=text,
            reply_markup=main_engineer_kb()
        )
    else:
        await message.answer(
            text=f"возникли непредвиденные ошибки, попробуйте снова:",
            reply_markup=main_engineer_kb()
        )
