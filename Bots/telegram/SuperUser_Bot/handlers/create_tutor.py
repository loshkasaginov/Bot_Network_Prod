import asyncio
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from Bots.logger.logger import logger
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.telegram.asinc_requests.asinc_requests import create_tutor
from Bots.telegram.SuperUser_Bot.keyboards.main_keyboard import main_superuser_kb


router = Router()

class AddTutor(StatesGroup):
    choosing_number = State()
    choosing_link = State()
    choosing_name = State()


@router.message(F.text.lower() == "добавить куратора")
async def add_tutor(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("Введите номер куратора:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddTutor.choosing_number)

@router.message(AddTutor.choosing_number)
async def number_chosen(message: Message, state: FSMContext):
    try :
        number = int(message.text.lower())
        await state.update_data(chosen_number=number)
        await message.answer(
            text="Спасибо. Теперь, пожалуйста, введите ссылку на куратора:",
        )
        await state.set_state(AddTutor.choosing_link)

    except:
        await message.answer(
            text="Введите номер куратора цифрами:",
        )
        await state.set_state(AddTutor.choosing_number)

@router.message(AddTutor.choosing_link)
async def link_chosen(message: Message, state: FSMContext):
    link = message.text.lower()
    await state.update_data(chosen_link=link)
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите имя куратора:",
    )
    await state.set_state(AddTutor.choosing_name)


@router.message(AddTutor.choosing_name)
async def name_chosen(message: Message, state: FSMContext):
    name = message.text.lower()
    await state.update_data(chosen_name=name)
    user_data = await state.get_data()
    data = {
        "tutors_number": user_data['chosen_number'],
        "link": user_data['chosen_link'],
        "name": user_data['chosen_name']
    }
    logger.info(
        f"user {str(message.from_user.url)} create_tutor")
    response = await create_tutor(data, str(message.from_user.url))
    if response:
        await message.answer(
            text=f"""Номер куратора: {user_data['chosen_number']} \nссылка на куратора: {user_data['chosen_link']}\nимя куратора: {user_data['chosen_name']}
            """,
            reply_markup=main_superuser_kb()
        )
        await state.clear()
    else:
        await message.answer(
            text="Ошибка Ввода куратора. Возможно куратор с таким номером или именем уже создан",
            reply_markup=main_superuser_kb()
        )
        await state.clear()
