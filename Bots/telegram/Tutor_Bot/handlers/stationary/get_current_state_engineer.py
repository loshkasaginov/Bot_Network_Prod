import asyncio
from aiogram import Router, F
from datetime import datetime
from aiogram.filters import Command, StateFilter
from aiogram.fsm import state
from Bots.logger.logger import logger
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.telegram.asinc_requests.asinc_requests import get_current_state_engineer_by_tutor
from Bots.telegram.Tutor_Bot.keyboards.main_keyboard import main_tutor_kb, engineers_tutor_kb


router = Router()


class GetCurrentEngineer(StatesGroup):
    choosing_engineers_number = State()

# @router.message(F.text.lower() == "посмотреть инженера")
# async def get_all_engineers(message: Message, state: FSMContext):
#     await message.answer(
#         text="Введите номер инженера:",
#     )
#     await state.set_state(GetCurrentEngineer.choosing_engineers_number)
#
# @router.message(GetCurrentEngineer.choosing_engineers_number)
# async def number_chosen(message: Message, state: FSMContext):
#     try:
#         await message.answer(
#             text=f"пожалуйста нажмите на /getstateengineer_{int(message.text.lower())}",
#             reply_markup=engineers_tutor_kb()
#         )
#         await state.clear()
#     except:
#         await message.answer(
#             text=f"пожалуйста введите номер инженера цифрами",
#         )
#         await state.set_state(GetCurrentEngineer.choosing_engineers_number)

@router.message(lambda message: message.text.startswith('/getstateengineer_'))
async def cmd_food(message: Message):
    command, state_engineers_number = message.text.split('_', 1)
    logger.info(
        f"user {str(message.from_user.url)} get_current_state_engineer_by_tutor params: state_engineers_number={state_engineers_number}")
    response = await get_current_state_engineer_by_tutor(state_engineers_number, str(message.from_user.url))
    if response:
        engineer = response
        engineer_info = f"Имя инженера: {engineer['name']}\n" \
                     f"номер инженера: {engineer['engineers_number']}\n" \
                     f"ссылка на инженера: {engineer['link']}\n\n"
        orders = ""
        if  engineer["orders"]:


            for order in engineer["orders"]:
                orders += f"заказ: {order['order_number']}, стадия: {order['stage_of_order']}\n" \
                         f"посмотреть заказ подробнее -> /getorder_{int(order['order_number'])}\n\n" \


        data = engineer_info + orders
        await message.answer(
                text=data,
                reply_markup=engineers_tutor_kb()
            )


    else:
        await message.answer(
            text=f"возникли непредвиденные ошибки, попробуйте снова:",
            reply_markup=engineers_tutor_kb()
        )


