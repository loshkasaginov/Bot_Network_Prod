from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.types import URLInputFile

from Bots.logger.logger import logger
from Bots.telegram.Tutor_Bot.keyboards.main_keyboard import orders_tutor_kb
from Bots.telegram.asinc_requests.asinc_requests import get_report_tutor_by_date

router = Router()

class OrderByDate(StatesGroup):
    choosing_start_time = State()
    choosing_end_time = State()

@router.message(F.text.lower() == "посмотреть все заказы по дате")
async def get_all_engineers(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="введите пожалуйста дату с которой нужно посмотреть заказы, в формате: год-месяц-число:",
        reply_markup=orders_tutor_kb()
    )
    await state.set_state(OrderByDate.choosing_start_time)

@router.message(OrderByDate.choosing_start_time)
async def engineers(message: Message, state: FSMContext):
    try:
        date_str = message.text.lower()
        start_date = datetime.strptime(date_str, "%Y-%m-%d") + timedelta(hours=0, minutes=0, seconds=0,
                                                                           milliseconds=0)
        date = start_date.isoformat() + 'Z'
        await state.update_data(start_date=date)
        await message.answer(
            text="введите пожалуйста дату до которой нужно посмотреть заказы, в формате: год-месяц-число:",
        )
        await state.set_state(OrderByDate.choosing_end_time)
    except:
        await message.answer(
            text="напишите дату в формате: год-месяц-число:",
        )
        await state.set_state(OrderByDate.choosing_start_time)

    @router.message(OrderByDate.choosing_end_time)
    async def engineers(message: Message, state: FSMContext):
        try:
            date_str = message.text.lower()
            start_date = datetime.strptime(date_str, "%Y-%m-%d") + timedelta(hours=0, minutes=0, seconds=0,
                                                                             milliseconds=0)
            date = start_date.isoformat() + 'Z'
            user_data = await state.get_data()
            logger.info(f'user {str(message.from_user.url)} get_report_tutor_by_date')
            response = await get_report_tutor_by_date(user_data["start_date"], date, str(message.from_user.url))
            if response:
                for report in response:

                    report_date_str = report['update_time'].rstrip('Z')
                    report_date = datetime.fromisoformat(report_date_str)
                    report_date_part = report_date.date()
                    report_time = report_date.strftime("%H:%M")

                    report_data = f"отчет:\n" \
                                  f"номер заказа: {report['order_number']}\n" \
                                  f"общая сумма: {report['all_amount']}\n" \
                                  f"сумма чистыми: {report['clear_amount']}\n" \
                                  f"сумма аванса: {report['advance_payment']}\n" \
                                  f"тип оплаты: {report['type_of_payment']}\n" \
                                  f"дата последнего обновления: {report_date_part}\n" \
                                  f"время последнего обновления: {report_time}\n"
                    try:
                        url = f"{report['photo_of_agreement']}"
                        photo = URLInputFile(url)
                        await message.answer_photo(photo, caption=report_data)
                    except:
                        await message.answer(
                            text=report_data,
                            reply_markup=orders_tutor_kb()
                        )
            else:
                await message.answer(
                    text="возникли ошибки",
                    reply_markup=orders_tutor_kb()
                )
            await state.clear()
        except:
            await message.answer(
                text="напишите дату в формате: год-месяц-число:",
            )
            await state.set_state(OrderByDate.choosing_end_time)






