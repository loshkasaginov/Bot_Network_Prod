import asyncio
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from Bots.logger.logger import logger
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, ContentType
from Bots.telegram.asinc_requests.asinc_requests import get_outlay_orders_engineer, create_outlay_record
from Bots.telegram.Engineer_Bot.keyboards.main_keyboard import main_engineer_kb, back_to_orders_engineer_kb,\
    agreement_engineer_kb, prepayment_type_engineer_kb
from aiogram.types import URLInputFile
from dotenv import load_dotenv
import os


router = Router()


class OutlayRecord(StatesGroup):
    choosing_number_outlays = State()
    choosing_name = State()
    choosing_cheque = State()
    choosing_tp_of_pmt = State()
    choosing_amount = State()
    choosing_way = State()


@router.message(F.text.lower() == "оприход")
async def engineers(message: Message):
    logger.info(
        f"user {str(message.from_user.url)} get_outlay_orders_engineer")
    response = await get_outlay_orders_engineer(str(message.from_user.url))
    if response:
        message_text = "Список заказов готовых для оприхода:\n\n"
        for order in response:
            order_info = f"Номер заказа: {order['order_number']} оприходывать -> /makeoutlay_{order['order_number']}\n\n"
            message_text += order_info
        await message.answer(
            text=message_text,
            reply_markup=back_to_orders_engineer_kb(),
        )
    else:
        await message.answer(
            text="Нет активных заказов на этой стадии, или ошибка доступа.",
            reply_markup=back_to_orders_engineer_kb()
        )


@router.message(lambda message: message.text and message.text.startswith('/makeoutlay_'))
async def cmd_food(message: Message, state: FSMContext):
    command, order_number = message.text.split('_', 1)
    await state.update_data(order_number=int(order_number), outlays=[], current_outlay=0)

    await message.reply(f"введите количество позиций для оприхода:")
    await state.set_state(OutlayRecord.choosing_number_outlays)


@router.message(OutlayRecord.choosing_number_outlays)
async def name_chosen(message: Message, state: FSMContext):
    try:
        number_of_forks=int(message.text.lower())
        if 25 > number_of_forks > 0:

            await state.update_data(number_of_outlays=int(message.text.lower()))
            await message.answer(
                text="Спасибо. Теперь, пожалуйста, 1 название:",
            )
            await state.set_state(OutlayRecord.choosing_name)
        else:
            await message.answer(
                text="введите, пожалуйста, цифру от 1 до 24:",
            )
            await state.set_state(OutlayRecord.choosing_number_outlays)
    except:
        await message.answer(
            text="введите, пожалуйста, цифру:",
        )
        await state.set_state(OutlayRecord.choosing_number_outlays)


@router.message(OutlayRecord.choosing_name)
async def name_chosen(message: Message, state: FSMContext):
    name = message.text.lower()
    await state.update_data(name=name)
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите сумму оприхода:",
    )
    await state.set_state(OutlayRecord.choosing_amount)



@router.message(OutlayRecord.choosing_amount)
async def name_chosen(message: Message, state: FSMContext):
    try:
        amount = int(message.text.lower())
    except:
        await message.answer(
            text="введите, пожалуйста, цифрами:",
        )
        await state.set_state(OutlayRecord.choosing_amount)
    await state.update_data(amount=amount)
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, пришлите одну фотографию чека:",
    )
    await state.set_state(OutlayRecord.choosing_cheque)




@router.message(OutlayRecord.choosing_cheque)
async def name_chosen(message: Message, state: FSMContext, bot):
    if message.photo:
        photo_info = message.photo[-1]
        photo_file = await bot.get_file(photo_info.file_id)
        load_dotenv()
        token = os.environ.get("ENGINEER_BOT_TOKEN")
        photo_url = f'https://api.telegram.org/file/bot{token}/{photo_file.file_path}'
        await state.update_data(cheque=photo_url)
        await message.answer(
            text="Спасибо. Теперь, пожалуйста, выберите способ оплаты:",
            reply_markup=prepayment_type_engineer_kb()
        )
        await state.set_state(OutlayRecord.choosing_tp_of_pmt)
    else:
        await message.answer(
            text="пришлите, пожалуйта, фотографию:",
        )
        await state.set_state(OutlayRecord.choosing_cheque)

@router.message(OutlayRecord.choosing_tp_of_pmt)
async def name_chosen(message: Message, state: FSMContext):
    if message.text.lower() == "наличные":
        await state.update_data(tp_of_pmt_id=2)
    elif message.text.lower() == "безнал":
        await state.update_data(tp_of_pmt_id=3)
    else:
        await message.answer(text="выберите еще раз",reply_markup=prepayment_type_engineer_kb())
        await state.set_state(OutlayRecord.choosing_tp_of_pmt)
    user_data = await state.get_data()
    current_outlay = user_data['current_outlay'] + 1
    outlays = user_data['outlays']
    outlays.append([user_data['name'],user_data['amount'],user_data['cheque'],user_data['tp_of_pmt_id']])


    if current_outlay < user_data['number_of_outlays']:
        await state.update_data(outlays=outlays, current_outlay=current_outlay)
        await message.answer(f"Введите позицию номер {current_outlay + 1}:")
        await state.set_state(OutlayRecord.choosing_name)
    else:
        outlay_record = []
        for outlay in outlays:
            data = {
                "name": outlay[0],
                "amount": outlay[1],
                "cheque": outlay[2],
                "tp_of_pmt_id": outlay[3]
            }
            outlay_record.append(data)
        final_data = {
            "order_number": user_data['order_number'],
            "outlays": outlay_record
        }
        logger.info(
            f"user {str(message.from_user.url)} create_outlay_record")
        response = await create_outlay_record(final_data, str(message.from_user.url))
        if response:
            await message.answer(text="Все варианты введены. Все данные успешно добавлены", reply_markup=main_engineer_kb(),)
            await state.clear()
        else:
            await message.answer(f"к сожалению, возникла ошибка при отправке данных. попробуйте снова:", reply_markup=main_engineer_kb(),)
            await state.clear()



# await message.answer(reply)_photo(photo=types.FSInputFile(photo_path))