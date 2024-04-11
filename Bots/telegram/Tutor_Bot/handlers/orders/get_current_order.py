import asyncio
import os
from aiogram import Router, F
from datetime import datetime
from aiogram.filters import Command, StateFilter
from aiogram.fsm import state
from Bots.logger.logger import logger
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types import FSInputFile, URLInputFile
from Bots.telegram.asinc_requests.asinc_requests import get_full_order_by_tutor
from Bots.telegram.Tutor_Bot.keyboards.main_keyboard import main_tutor_kb, orders_tutor_kb
from PIL import Image

router = Router()

class GetCurrentOrder(StatesGroup):
    choosing_order_number = State()

@router.message(F.text.lower() == "посмотреть заказ")
async def get_all_engineers(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Введите номер заказа:",
    )
    await state.set_state(GetCurrentOrder.choosing_order_number)

@router.message(GetCurrentOrder.choosing_order_number)
async def number_chosen(message: Message, state: FSMContext):
    try:
        await message.answer(
            text=f"пожалуйста нажмите на /getorder_{int(message.text.lower())}",
            reply_markup=orders_tutor_kb()
        )
        await state.clear()
    except:
        await message.answer(
            text=f"пожалуйста введите номер заказа цифрами",
        )
        await state.set_state(GetCurrentOrder.choosing_order_number)

@router.message(lambda message: message.text.startswith('/getorder_'))
async def cmd_food(message: Message, state: FSMContext, bot):
    await state.clear()
    command, order_number = message.text.split('_', 1)
    logger.info(f"user {str(message.from_user.url)} get_full_order_by_tutor params: order_number={order_number}")
    response = await get_full_order_by_tutor(order_number, str(message.from_user.url))
    if response:
        order = response
        date_str = order['update_time'].rstrip('Z')
        date = datetime.fromisoformat(date_str)
        date_part = date.date()
        time = date.strftime("%H:%M")
        order_info = f"Номер заказа: {order['order_number']}\n" \
                     f"Имя инженера: {order['engineers_name']}\n" \
                     f"номер инженера: {order['engineers_number']}\n" \
                     f"стадия заказа: {order['stage_of_order']}\n" \
                     f"дата последнего обновления: {date_part}\n" \
                     f"время последнего обновления: {time}\n"
        await message.answer(
        text=order_info,
        )
        if  order["details"]["agreement"]:
            forks = ""
            rejection = ""
            agreement_date_str = order['details']['agreement']['update_time'].rstrip('Z')
            agreement_date = datetime.fromisoformat(agreement_date_str)
            agreement_date_part = agreement_date.date()
            agreement_time = agreement_date.strftime("%H:%M")
            for fork in order["details"]["agreement"]["agreement_details"]["forks"]:
                forks += f"описание позиции:\n" \
                         f"описание вилки: {fork['description']}\n" \
                         f"предложенная цена: {fork['amount']}\n\n"


            if order["details"]["agreement"]["agreement_details"]["rejection"]:
                rejection += f"описание отказа: {order['details']['agreement']['agreement_details']['rejection']['description']}\n"

            agreement_data = f"согласование:\n" \
                            f"дата последнего обновления: {agreement_date_part}\n" \
                            f"время последнего обновления: {agreement_time}\n" \
                            f"итоговая согласованная сумма: {order['details']['agreement']['amount']}\n" \
                            f"Вилка цен:\n\n"  + forks + rejection
            await message.answer(
                text=agreement_data,
                reply_markup=orders_tutor_kb()
            )
        if order["details"]["prepayment"]:
            prepayment_date_str = order['details']['prepayment']['update_time'].rstrip('Z')
            prepayment_date = datetime.fromisoformat(prepayment_date_str)
            prepayment_date_part = prepayment_date.date()
            prepayment_time = prepayment_date.strftime("%H:%M")
            prepayment = f"предоплата:\n" \
                         f"сумма предоплаты: {order['details']['prepayment']['amount']}\n" \
                         f"тип предоплаты: {order['details']['prepayment']['type_of_payment']}\n" \
                         f"дата последнего обновления: {prepayment_date_part}\n" \
                         f"время последнего обновления: {prepayment_time}\n" \

            await message.answer(
                text=prepayment,
                reply_markup=orders_tutor_kb()
            )
        if order["details"]["stationary"]:
            stationary_date_str = order['details']['stationary']['update_time'].rstrip('Z')
            stationary_date = datetime.fromisoformat(stationary_date_str)
            stationary_date_part = stationary_date.date()
            stationary_time = stationary_date.strftime("%H:%M")
            sate_date_str = order['details']['stationary']['date'].rstrip('Z')
            state_date = datetime.fromisoformat(sate_date_str)
            state_date_part = state_date.date()
            s = order['details']['stationary']
            stationary = f"стационар:\n" \
                         f"номер стационарного инженеар: {s['state_engineers_number']}\n" \
                         f"выполнить до: {state_date_part}\n" \
                         f"приоритет: {s['priority']}\n" \
                         f"описание: {s['description']}\n" \
                         f"сумма: {s['amount']}\n" \
                         f"дата последнего обновления: {stationary_date_part}\n" \
                         f"время последнего обновления: {stationary_time}\n" \

            try:
                url = f"{s['photo']}"
                photo = URLInputFile(url)
                await message.answer_photo(photo, caption=stationary)
            except:
                await message.answer(
                    text=stationary,
                    reply_markup=orders_tutor_kb()
                )
        if order["details"]["outlay_record"]:
            for outlay in order["details"]["outlay_record"]:
                outlay_date_str = outlay['update_time'].rstrip('Z')
                outlay_date = datetime.fromisoformat(outlay_date_str)
                outlay_date_part = outlay_date.date()
                outlay_time = outlay_date.strftime("%H:%M")

                outlay_data = f"оприход:\n" \
                            f"название оприхода: {outlay['name']}\n" \
                            f"сумма оприхода: {outlay['amount']}\n" \
                         f"тип оприхода: {outlay['type_of_payment']}\n" \
                         f"дата последнего обновления: {outlay_date_part}\n" \
                         f"время последнего обновления: {outlay_time}\n" \

                # with Image.open("photo.jpg") as im:
                #     im.show()
                try:
                    url = f"{outlay['cheque']}"
                    photo = URLInputFile(url)
                    await message.answer_photo(photo, caption=outlay_data)
                except:
                    await message.answer(
                        text=outlay_data,
                        reply_markup=orders_tutor_kb()
                    )

        if order["details"]["report"]:
            report = order["details"]["report"]
            report_date_str = report['update_time'].rstrip('Z')
            report_date = datetime.fromisoformat(report_date_str)
            report_date_part = report_date.date()
            report_time = report_date.strftime("%H:%M")

            report_data = f"отчет:\n" \
                        f"общая сумма: {report['all_amount']}\n" \
                        f"сумма чистыми: {report['clear_amount']}\n" \
                          f"сумма аванса: {report['advance_payment']}\n"\
                          f"тип оплаты: {report['type_of_payment']}\n" \
                     f"дата последнего обновления: {report_date_part}\n" \
                     f"время последнего обновления: {report_time}\n" \


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
            text=f"возникли непредвиденные ошибки, попробуйте снова:",
            reply_markup=orders_tutor_kb()
        )
        await state.clear()


