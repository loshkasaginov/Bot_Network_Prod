import asyncio
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from Bots.logger.logger import logger
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.logger.logger import logger
from Bots.telegram.asinc_requests.asinc_requests import create_order
from Bots.telegram.Tutor_Bot.keyboards.main_keyboard import main_tutor_kb


router = Router()

class AddOrder(StatesGroup):
    choosing_engineer_number = State()
    choosing_order_number = State()


@router.message(F.text.lower() == "добавить заказ")
async def add_order(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("Введите имя инженера:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddOrder.choosing_engineer_number)

@router.message(AddOrder.choosing_engineer_number)
async def number_chosen(message: Message, state: FSMContext):

    name = message.text.lower()
    await state.update_data(chosen_engineers_name=name)
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите номер заказа:",
    )
    await state.set_state(AddOrder.choosing_order_number)


@router.message(AddOrder.choosing_order_number)
async def name_chosen(message: Message, state: FSMContext):
    try :
        order_number = int(message.text.lower())
        await state.update_data(chosen_order_number=order_number)
        user_data = await state.get_data()
    except:
        await message.answer(
            text="Введите номер заказа цифрами:",
        )
        await state.set_state(AddOrder.choosing_order_number)
    data = {
        "engineers_name": user_data['chosen_engineers_name'],
        "order_number": user_data['chosen_order_number'],
    }
    logger.info(f"user {str(message.from_user.url)} create_order params: engineers_name={user_data['chosen_engineers_name']}, order_number={user_data['chosen_order_number']}")
    response = await create_order(data, str(message.from_user.url))
    if response:
        await message.answer(
            text=f"""имя инженера: {user_data['chosen_engineers_name']} \nномер заказа: {user_data['chosen_order_number']}
            """,
            reply_markup=main_tutor_kb()
        )
        await state.clear()
    else:
        await message.answer(
            text="Ошибка Ввода инженера. Возможно заказ с таким номером или инженером уже создан",
            reply_markup=main_tutor_kb()
        )
        await state.clear()



