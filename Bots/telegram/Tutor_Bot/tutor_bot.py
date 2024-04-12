import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from Bots.DB.sqlite_db import Db
from Bots.logger.logger import logger
from Bots.telegram.Tutor_Bot.handlers import auth, keyboards_logic
from Bots.telegram.Tutor_Bot.handlers.engineers import create_engineer, get_engineers, delete_engineer, \
    get_current_engineer
from Bots.telegram.Tutor_Bot.handlers.orders import order_create, get_orders, get_current_order, get_orders_by_date
from Bots.telegram.Tutor_Bot.handlers.stages import agreements, prepayments, outlays, report
from Bots.telegram.Tutor_Bot.handlers.stationary import create_state_engineer, delete_satate_engineer, \
    get_state_engineers, \
    get_state_orders, get_current_state_engineer
from Bots.telegram.asinc_requests.asinc_requests import refresh_access_tokens


async def create_db():
    db = Db()
    await db.create_users_table()


async def periodic_task():
    while True:
        logger.info(f'Tutor bot refresh_access_tokens')
        await refresh_access_tokens()
        await asyncio.sleep(20 * 60 * 60)

async def main():
    await create_db()
    dp = Dispatcher(storage=MemoryStorage())
    load_dotenv()
    bot = Bot(token=os.environ.get("TUTOR_BOT_TOKEN"))
    dp.include_router(auth.router)
    dp.include_router(keyboards_logic.router)
    dp.include_router(create_engineer.router)
    dp.include_router(get_engineers.router)
    dp.include_router(delete_engineer.router)
    dp.include_router(order_create.router)
    dp.include_router(get_orders.router)
    dp.include_router(get_current_order.router)
    dp.include_router(get_current_engineer.router)
    dp.include_router(create_state_engineer.router)
    dp.include_router(delete_satate_engineer.router)
    dp.include_router(get_state_engineers.router)
    dp.include_router(get_state_orders.router)
    dp.include_router(agreements.router)
    dp.include_router(prepayments.router)
    dp.include_router(outlays.router)
    dp.include_router(report.router)
    dp.include_router(get_current_state_engineer.router)
    dp.include_router(get_orders_by_date.router)
    logger.info(f'Tutor bot started')
    await asyncio.gather(
        dp.start_polling(bot),
        periodic_task()
    )
    # await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
