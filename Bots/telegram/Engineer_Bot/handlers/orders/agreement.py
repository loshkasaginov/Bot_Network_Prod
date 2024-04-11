import asyncio
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from Bots.logger.logger import logger
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from Bots.telegram.asinc_requests.asinc_requests import get_agreement_orders_engineer, create_agreement
from Bots.telegram.Engineer_Bot.keyboards.main_keyboard import main_engineer_kb, back_to_orders_engineer_kb, agreement_engineer_kb


router = Router()


class Agreement(StatesGroup):
    choosing_number_fork = State()
    choosing_fork = State()
    choosing_amount = State()
    choosing_final_amount = State()
    choosing_rejection = State()
    choosing_way = State()


@router.message(F.text.lower() == "согласование")
async def engineers(message: Message):
    logger.info(
        f"user {str(message.from_user.url)} get_agreement_orders_engineer")
    response = await get_agreement_orders_engineer(str(message.from_user.url))
    if response:
        message_text = "Список заказов готовых для согласования:\n\n"
        for order in response:
            order_info = f"Номер заказа: {order['order_number']} согласовать -> /makeagreement_{order['order_number']}\n\n"
            message_text += order_info
        await message.answer(
            text=message_text,
            reply_markup=back_to_orders_engineer_kb(),
        )
    else:
        await message.answer(
            text="Нет активных заказов на этой стадии, или ошибка доступа.",
            reply_markup=main_engineer_kb()
        )


@router.message(lambda message: message.text and message.text.startswith('/makeagreement_'))
async def cmd_food(message: Message, state: FSMContext):
    command, order_number = message.text.split('_', 1)
    await state.update_data(order_number=int(order_number), forks=[], current_fork=0)

    await message.reply(f"введите количество вариантов, предложенных клиенту:")
    await state.set_state(Agreement.choosing_number_fork)


@router.message(Agreement.choosing_number_fork)
async def name_chosen(message: Message, state: FSMContext):
    try:
        number_of_forks=int(message.text.lower())
        if 10 > number_of_forks > 0:

            await state.update_data(number_of_forks=int(message.text.lower()))
            await message.answer(
                text="Спасибо. Теперь, пожалуйста, введите 1 предложенный клиенту вариант:",
            )
            await state.set_state(Agreement.choosing_fork)
        else:
            await message.answer(
                text="введите, пожалуйста, цифру от 1 до 9:",
            )
            await state.set_state(Agreement.choosing_number_fork)
    except:
        await message.answer(
            text="введите, пожалуйста, цифру:",
        )
        await state.set_state(Agreement.choosing_number_fork)

@router.message(Agreement.choosing_fork)
async def name_chosen(message: Message, state: FSMContext):
    text = message.text.lower()
    await state.update_data(text=text)
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите сумму для этого варианта:",
    )
    await state.set_state(Agreement.choosing_amount)

@router.message(Agreement.choosing_amount)
async def name_chosen(message: Message, state: FSMContext):
    try:
        amount = int(message.text.lower())
    except:
        await message.answer(
            text="введите, пожалуйста, цифрами:",
        )
        await state.set_state(Agreement.choosing_amount)

    user_data = await state.get_data()
    current_fork = user_data['current_fork'] + 1
    forks = user_data['forks']
    forks.append([user_data['text'], amount])
    if current_fork < user_data['number_of_forks']:
        await state.update_data(forks=forks, current_fork=current_fork)
        await message.answer(f"Введите вариант номер {current_fork + 1}:")
        await state.set_state(Agreement.choosing_fork)
    else:
        await state.update_data(forks=forks)
        await message.answer(text="Все варианты введены. вам удалось согласовать, или случился отказ?", reply_markup=agreement_engineer_kb(),)
        await state.set_state(Agreement.choosing_way)



@router.message(Agreement.choosing_way,F.text.lower() == "удалось согласовать")
async def engineers(message: Message, state: FSMContext):
    await message.reply(f"введите конечную сумму:")
    await state.set_state(Agreement.choosing_final_amount)




@router.message(Agreement.choosing_way, F.text.lower() == "отказ")
async def engineers(message: Message, state: FSMContext):
    await message.reply(f"введите причину отказа:")
    await state.set_state(Agreement.choosing_rejection)


@router.message(Agreement.choosing_rejection)
async def name_chosen(message: Message, state: FSMContext):
    rejection = message.text.lower()
    await state.update_data(rejection=rejection)
    await message.reply(f"введите сумму отказа:")
    await state.set_state(Agreement.choosing_final_amount)


@router.message(Agreement.choosing_final_amount)
async def name_chosen(message: Message, state: FSMContext):
    try:
        final_amount=int(message.text.lower())
        await state.update_data(final_amount=final_amount)
    except:
        await message.answer(
            text="введите, пожалуйста, цифрами:",
        )
        await state.set_state(Agreement.choosing_final_amount)
    user_data = await state.get_data()
    forks = []
    for i in user_data['forks']:
        forks.append({"amount": int(i[1]), "description": str(i[0])})
    try:
        user_data['rejection']
        data = {
            "order_number": int(user_data['order_number']),
            "amount": int(user_data['final_amount']),
            "agreement_details": {
                "forks": forks,
                "rejection": {
                    "amount": int(user_data['final_amount']),
                    "description": str(user_data['rejection'])
                }
            }
        }
        logger.info(
            f"user {str(message.from_user.url)} engineer_auth params: user_name={user_data['chosen_user_name']}")
        response = await create_agreement(data, str(message.from_user.url))
    except:
        data = {
            "order_number": user_data['order_number'],
            "amount": user_data['final_amount'],
            "agreement_details": {
                "forks": forks,
            }
        }
        logger.info(
            f"user {str(message.from_user.url)} create_agreement")
        response = await create_agreement(data, str(message.from_user.url))

    if response:
        await message.answer(
            text=f"согласование успешно создано",
            reply_markup=main_engineer_kb()
        )
        await state.clear()
    else:
        await message.answer(
            text=f"возникли непредвиденные ошибки, попробуйте снова.:",
            reply_markup=main_engineer_kb()
        )
        await state.clear()
