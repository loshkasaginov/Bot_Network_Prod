
from datetime import datetime
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from Bots.logger.logger import logger
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.telegram.asinc_requests.asinc_requests import get_stationary_orders_tutor, change_priority_stationary_tutor
from Bots.telegram.Tutor_Bot.keyboards.main_keyboard import stationary_tutor_kb
from aiogram.types import FSInputFile, URLInputFile

router = Router()


@router.message(F.text.lower() == "посмотреть все заказы в стационаре")
async def get_all_engineers(message: Message):
    logger.info(f"user {str(message.from_user.url)} get_stationary_orders_tutor")
    response = await get_stationary_orders_tutor(str(message.from_user.url))
    if response:
        await message.answer(
            text="список заказов.",
        )
        for order in response:
            date_str = order['update_time'].rstrip('Z')
            date = datetime.fromisoformat(date_str)
            date_part = date.date()
            time = date.strftime("%H:%M")
            sate_date_str = order['date'].rstrip('Z')
            state_date = datetime.fromisoformat(sate_date_str)
            state_date_part = state_date.date()
            order_info = f"Номер заказа: {order['order_number']}\n" \
                         f"номер инженера: {order['engineers_number']}\n" \
                         f"номер стационарного инженера: {order['state_engineers_number']}\n" \
                         f"приоритет: {order['priority']}\n" \
                         f"описание: {order['description']}\n" \
                         f"выполнить до: {state_date_part}\n" \
                         f"дата последнего обновления: {date_part}\n" \
                         f"время последнего обновления: {time}\n" \
                         f"посмотреть детали заказа -> /getorder_{order['order_number']}\n\n" \
                         f"назначить другой приоритет -> /priority_{order['order_number']}\n\n"
            try:
                url = f"{order['photo']}"
                photo = URLInputFile(url)
                await message.answer_photo(photo, caption=order_info)
            except:
                await message.answer(
                    text=order_info,
                    reply_markup=stationary_tutor_kb()
                )
    else:
        await message.answer(
            text="Ошибка доступа.",
            reply_markup=stationary_tutor_kb()
        )

class Priority(StatesGroup):
    choosing_priority = State()



@router.message(lambda message: message.text.startswith('/priority_'))
async def cmd_food(message: Message, state: FSMContext):
    command, order_number = message.text.split('_', 1)
    await state.update_data(order_number=int(order_number))
    await message.reply(text=f"введите новый приоритет")
    await state.set_state(Priority.choosing_priority)



@router.message(Priority.choosing_priority)
async def engineers(message: Message, state: FSMContext):
    user_data = await state.get_data()
    data = {
        "order_number": user_data['order_number'],
        "priority": int(message.text),
    }
    logger.info(f"user {str(message.from_user.url)} change_priority_stationary_tutor params: order_number={user_data['order_number']}, priority={int(message.text)}")
    response = await change_priority_stationary_tutor(data, str(message.from_user.url))
    if response:
        await message.reply(text=f"приоритет успешно сменен:", reply_markup=stationary_tutor_kb())
    else:
        await message.reply(text=f"возникла ошибка при смене приоритета:", reply_markup=stationary_tutor_kb())
    await state.clear()