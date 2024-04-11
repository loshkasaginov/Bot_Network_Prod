import asyncio
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from Bots.logger.logger import logger
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.telegram.asinc_requests.asinc_requests import engineer_auth
from Bots.telegram.Engineer_Bot.keyboards.main_keyboard import main_engineer_kb


router = Router()


class EngineerAuth(StatesGroup):
    choosing_name = State()
    choosing_password = State()


@router.message(Command("start"))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Введите свой логин:",
    )
    await state.set_state(EngineerAuth.choosing_name)


@router.message(EngineerAuth.choosing_name)
async def name_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_user_name=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите свой пароль:",
    )
    await state.set_state(EngineerAuth.choosing_password)


@router.message(EngineerAuth.choosing_password)
async def food_size_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(chosen_password=message.text.lower())
    data = {
        "user_name": user_data['chosen_user_name'],
        "password": message.text.lower(),
    }
    logger.info(
        f"user {str(message.from_user.url)} engineer_auth params: user_name={user_data['chosen_user_name']}")
    response = await engineer_auth(data, str(message.from_user.url))
    if response:
        await message.answer(
            text=f"Ваш логин:{user_data['chosen_user_name']} Ваш пароль: {message.text.lower()}.\n",
            reply_markup=main_engineer_kb()
        )
        await state.clear()
    else:
        await message.answer(
            text=f"Неверный логин или пароль. попробуйте заного. Введите логин:",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(EngineerAuth.choosing_name)



