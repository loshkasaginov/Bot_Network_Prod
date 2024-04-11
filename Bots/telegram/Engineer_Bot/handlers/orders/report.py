import asyncio
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from Bots.logger.logger import logger
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.telegram.asinc_requests.asinc_requests import get_report_orders_engineer, create_report
from Bots.telegram.Engineer_Bot.keyboards.main_keyboard import main_engineer_kb, \
    back_to_orders_engineer_kb, orders_engineer_kb, report_engineer_kb, report_type_engineer_kb
from dotenv import load_dotenv
import os

router = Router()


class Report(StatesGroup):
    choosing_amount = State()
    choosing_final_amount = State()
    choosing_advance_payment = State()
    choosing_tp_of_pmt = State()
    choosing_way = State()
    choosing_photo = State()



@router.message(F.text.lower() == "отчет")
async def engineers(message: Message):
    logger.info(
        f"user {str(message.from_user.url)} get_report_orders_engineer")
    response = await get_report_orders_engineer(str(message.from_user.url))
    if response:
        message_text = "Список заказов готовых для отчета::\n\n"
        for order in response:
            order_info = f"Номер заказа: {order['order_number']} сделать отчет -> /makereport_{order['order_number']}\n\n"
            message_text += order_info
        await message.answer(
            text=message_text,
            reply_markup=back_to_orders_engineer_kb(),
        )
    else:
        await message.answer(
            text="Нет активных заказов на этой стадии, или ошибка доступа.",
            reply_markup=orders_engineer_kb()
        )


@router.message(lambda message: message.text and message.text.startswith('/makereport_'))
async def cmd_food(message: Message, state: FSMContext):
    command, order_number = message.text.split('_', 1)
    await state.update_data(order_number=int(order_number))

    await message.reply(text=f"фото договора есть?", reply_markup=report_engineer_kb())
    await state.set_state(Report.choosing_way)

@router.message(Report.choosing_way,F.text.lower() == "договор есть")
async def engineers(message: Message, state: FSMContext):
    await message.reply(text=f"пришлите фото договора:",reply_markup=back_to_orders_engineer_kb())
    await state.set_state(Report.choosing_photo)

@router.message(Report.choosing_way,F.text.lower() == "без договора")
async def engineers(message: Message, state: FSMContext):
    await message.reply(text=f"напишите полную сумму заказа:",reply_markup=back_to_orders_engineer_kb())
    await state.update_data(photo_of_agreement=None)
    await state.set_state(Report.choosing_amount)

@router.message(Report.choosing_photo)
async def engineers(message: Message, state: FSMContext, bot):
    if message.photo:
        photo_info = message.photo[-1]
        photo_file = await bot.get_file(photo_info.file_id)
        load_dotenv()
        token = os.environ.get("ENGINEER_BOT_TOKEN")
        photo_url = f'https://api.telegram.org/file/bot{token}/{photo_file.file_path}'
        await state.update_data(photo_of_agreement=photo_url)
        await message.reply(text=f"напишите полную сумму:", reply_markup=back_to_orders_engineer_kb())
        await state.set_state(Report.choosing_amount)
    else:
        await message.reply(text=f"пришлите пожалуйтста фото:", reply_markup=back_to_orders_engineer_kb())
        await state.set_state(Report.choosing_photo)






@router.message(Report.choosing_amount)
async def engineers(message: Message, state: FSMContext):
    try:
        amount = int(message.text.lower())
    except:
        await message.answer(
            text="введите, пожалуйста, цифрами:",
        )
        await state.set_state(Report.choosing_amount)
    await state.update_data(amount=amount)
    await message.answer(
        text="теперь напишите чистую сумму заказа:",
        reply_markup = back_to_orders_engineer_kb()
    )
    await state.set_state(Report.choosing_final_amount)

@router.message(Report.choosing_final_amount)
async def engineers(message: Message, state: FSMContext):
    try:
        amount = int(message.text.lower())
    except:
        await message.answer(
            text="введите, пожалуйста, цифрами:",
        )
        await state.set_state(Report.choosing_final_amount)
    await state.update_data(final_amount=amount)
    await message.answer(
        text="теперь выберите вид оплаты:",
        reply_markup = report_type_engineer_kb()
    )
    await state.set_state(Report.choosing_tp_of_pmt)


@router.message(Report.choosing_tp_of_pmt, F.text.lower() == "наличные")
async def engineers(message: Message, state: FSMContext):
    await state.update_data(tp_of_pmt_id=1)
    await message.answer(
        text="теперь введите аванс который хотите взять:",
        reply_markup=back_to_orders_engineer_kb()
    )
    await state.set_state(Report.choosing_advance_payment)

@router.message(Report.choosing_tp_of_pmt, F.text.lower() == "бн оплачен")
async def engineers(message: Message, state: FSMContext):
    await state.update_data(tp_of_pmt_id=2)
    await message.answer(
        text="теперь введите аванс который хотите взять:",
        reply_markup=back_to_orders_engineer_kb()
    )
    await state.set_state(Report.choosing_advance_payment)

@router.message(Report.choosing_advance_payment)
async def engineers(message: Message, state: FSMContext):
    try:
        advance_payment = int(message.text.lower())
    except:
        await message.answer(
            text="введите, пожалуйста, цифрами:",
        )
        await state.set_state(Report.choosing_advance_payment)
    await state.update_data(advance_payment=advance_payment)
    user_data = await state.get_data()
    data={
        "order_number": user_data['order_number'],
        "all_amount": user_data['amount'],
        "clear_amount": user_data['final_amount'],
        "photo_of_agreement": user_data['photo_of_agreement'],
        "advance_payment": user_data['advance_payment'],
        "tp_of_pmt_id":user_data['tp_of_pmt_id']
    }
    logger.info(
        f"user {str(message.from_user.url)} create_report")
    response = await create_report(data, str(message.from_user.url))
    if response:
        await message.reply(text=f"отчет успешно создан:", reply_markup=orders_engineer_kb())
    else:
        await message.reply(text=f"возникла ошибка при отчитывании:", reply_markup=orders_engineer_kb())
    await state.clear()

