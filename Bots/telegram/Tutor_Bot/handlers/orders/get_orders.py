from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from Bots.logger.logger import logger
from Bots.telegram.Tutor_Bot.keyboards.main_keyboard import orders_tutor_kb
from Bots.telegram.asinc_requests.asinc_requests import get_short_orders_by_tutor

router = Router()


@router.message(F.text.lower() == "посмотреть все заказы")
async def get_all_engineers(message: Message, state: FSMContext):
    logger.info(f'user {str(message.from_user.url)} get_short_orders_by_tutor')
    await state.clear()
    response = await get_short_orders_by_tutor(str(message.from_user.url))
    if response:
        message_text = "Список заказов:\n\n"
        for order in response:
            date_str = order['update_time'].rstrip('Z')
            date = datetime.fromisoformat(date_str)
            date_part = date.date()
            time = date.strftime("%H:%M")
            order_info = f"Номер заказа: {order['order_number']}\n" \
                         f"Имя инженера: {order['name']}\n" \
                         f"номер инженера: {order['engineers_number']}\n" \
                         f"стадия заказа: {order['stage_of_order']}\n" \
                         f"дата последнего обновления: {date_part}\n" \
                         f"время последнего обновления: {time}\n" \
                         f"посмотреть детали заказа -> /getorder_{order['order_number']}\n\n"
            message_text += order_info
        await message.answer(
            text=message_text,
            reply_markup=orders_tutor_kb()
        )
    else:
        await message.answer(
            text="Ошибка доступа.",
            reply_markup=orders_tutor_kb()
        )
