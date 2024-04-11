import asyncio
from aiogram import Router, F
from datetime import datetime
from aiogram.filters import Command, StateFilter
from Bots.logger.logger import logger
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.telegram.asinc_requests.asinc_requests import get_current_engineer_by_tutor, make_penalty_tutor, get_penalty_tutor
from Bots.telegram.Tutor_Bot.keyboards.main_keyboard import main_tutor_kb, engineers_tutor_kb


router = Router()


class GetCurrentEngineer(StatesGroup):
    choosing_engineers_number = State()

@router.message(F.text.lower() == "посмотреть инженера")
async def get_all_engineers(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Введите номер инженера:",
    )
    await state.set_state(GetCurrentEngineer.choosing_engineers_number)

@router.message(GetCurrentEngineer.choosing_engineers_number)
async def number_chosen(message: Message, state: FSMContext):
    try:
        await message.answer(
            text=f"пожалуйста нажмите на /getengineer_{int(message.text.lower())}",
            reply_markup=engineers_tutor_kb()
        )
        await state.clear()
    except:
        await message.answer(
            text=f"пожалуйста введите номер инженера цифрами",
        )
        await state.set_state(GetCurrentEngineer.choosing_engineers_number)

@router.message(lambda message: message.text.startswith('/getengineer_'))
async def cmd_food(message: Message, state: FSMContext):
    await state.clear()
    command, engineers_number = message.text.split('_', 1)
    logger.info(f"user {str(message.from_user.url)} get_current_engineer_by_tutor params: engineers_number={engineers_number}")
    response = await get_current_engineer_by_tutor(engineers_number, str(message.from_user.url))
    if response:
        engineer = response
        engineer_info = f"Имя инженера: {engineer['name']}\n" \
                     f"номер инженера: {engineer['engineers_number']}\n" \
                     f"ссылка на инженера: {engineer['link']}\n\n" \
                        f"посмотреть штрафы: /showpenalty_{engineer['engineers_number']}\n" \
                        f"назначить штраф: /makepenalty_{engineer['engineers_number']}\n"
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

class MakePenaltyEngineer(StatesGroup):
    choosing_amount = State()
    choosing_description = State()

@router.message(lambda message: message.text.startswith('/makepenalty_'))
async def cmd_food(message: Message, state: FSMContext):
    command, engineers_number = message.text.split('_', 1)
    await state.update_data(engineers_number=engineers_number)
    await message.answer(
        text=f"введите сумму штрафа которую хотите назначить:",
    )
    await state.set_state(MakePenaltyEngineer.choosing_amount)

@router.message(MakePenaltyEngineer.choosing_amount)
async def number_chosen(message: Message, state: FSMContext):
    try:
        await state.update_data(amount=int(message.text.lower()))
        await message.answer(
            text=f"пожалуйста, введите описание штрафа",
        )
        await state.set_state(MakePenaltyEngineer.choosing_description)
    except:
        await message.answer(
            text=f"пожалуйста введите сумму цифрами",
        )
        await state.set_state(MakePenaltyEngineer.choosing_amount)

@router.message(MakePenaltyEngineer.choosing_description)
async def number_chosen(message: Message, state: FSMContext):
    await state.update_data(description=message.text.lower())
    penalty_data = await state.get_data()
    data = {
        "engineers_number": penalty_data["engineers_number"],
        "amount": penalty_data["amount"],
        "description": penalty_data["description"],
    }
    logger.info(f"user {str(message.from_user.url)} make_penalty_tutor params: engineers_number={penalty_data['engineers_number']}, amount={penalty_data['amount']}")
    response = await make_penalty_tutor(data, str(message.from_user.url))
    if response:
        await message.answer(
            text=f"штраф успешно назначен:",
            reply_markup=engineers_tutor_kb()
        )
    else:
        await message.answer(
            text=f"возникли непредвиденные ошибки, попробуйте снова:",
            reply_markup=engineers_tutor_kb()
        )
    await state.clear()


@router.message(lambda message: message.text.startswith('/showpenalty_'))
async def cmd_food(message: Message, state: FSMContext):
    await state.clear()
    command, engineers_number = message.text.split('_', 1)
    logger.info(
        f"user {str(message.from_user.url)} get_penalty_tutor params: engineers_number={engineers_number}")
    response = await get_penalty_tutor(engineers_number,str(message.from_user.url))
    if response:
        text = "штрафы:\n\n"
        for penalty in response:
            penalty_date_str = penalty['update_time'].rstrip('Z')
            penalty_date = datetime.fromisoformat(penalty_date_str)
            penalty_date_part = penalty_date.date()
            penalty_time = penalty_date.strftime("%H:%M")

            text+=f"сумма штрафа: {penalty['amount']}\n" \
                  f"описание: {penalty['description']}\n"\
                  f"дата добавления: {penalty_date_part}\n" \
                  f"время добавления: {penalty_time}\n\n"
        await message.answer(
            text=text,
            reply_markup=engineers_tutor_kb()
        )
    else:
        await message.answer(
            text=f"возникли непредвиденные ошибки, попробуйте снова:",
            reply_markup=engineers_tutor_kb()
        )


