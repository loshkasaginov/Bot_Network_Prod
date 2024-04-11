import asyncio
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.logger.logger import logger
from Bots.telegram.asinc_requests.asinc_requests import create_engineer
from Bots.telegram.Tutor_Bot.keyboards.main_keyboard import main_tutor_kb


router = Router()

class AddEngineer(StatesGroup):
    choosing_number = State()
    choosing_link = State()
    choosing_name = State()


@router.message(F.text.lower() == "добавить инженера")
async def add_tutor(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("Введите номер инженера:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddEngineer.choosing_number)

@router.message(AddEngineer.choosing_number)
async def number_chosen(message: Message, state: FSMContext):
    try :
        number = int(message.text.lower())
        await state.update_data(chosen_number=number)
        await message.answer(
            text="Спасибо. Теперь, пожалуйста, введите ссылку на инженера:",
        )
        await state.set_state(AddEngineer.choosing_link)

    except:
        await message.answer(
            text="Введите номер инженера цифрами:",
        )
        await state.set_state(AddEngineer.choosing_number)

@router.message(AddEngineer.choosing_link)
async def link_chosen(message: Message, state: FSMContext):
    link = message.text.lower()
    await state.update_data(chosen_link=link)
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите имя инженера:",
    )
    await state.set_state(AddEngineer.choosing_name)


@router.message(AddEngineer.choosing_name)
async def name_chosen(message: Message, state: FSMContext):
    name = message.text.lower()
    await state.update_data(chosen_name=name)
    user_data = await state.get_data()
    data = {
        "engineers_number": user_data['chosen_number'],
        "link": user_data['chosen_link'],
        "name": user_data['chosen_name']
    }
    logger.info(f"user {str(message.from_user.url)} create_engineer params: engineers_number={user_data['chosen_number']}, link={user_data['chosen_link']}, name={user_data['chosen_name']}")
    response = await create_engineer(data, str(message.from_user.url))
    if response:
        await message.answer(
            text=f"""Номер инженера: {user_data['chosen_number']} \nссылка на инженера: {user_data['chosen_link']}\nимя инженера: {user_data['chosen_name']}
            """,
            reply_markup=main_tutor_kb()
        )
        await state.clear()
    else:
        await message.answer(
            text="Ошибка Ввода инженера. Возможно инженера с таким номером или именем уже создан",
            reply_markup=main_tutor_kb()
        )
        await state.clear()
