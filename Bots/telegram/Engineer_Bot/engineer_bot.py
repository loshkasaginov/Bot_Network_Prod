import asyncio
import logging
from aiogram import Bot, Dispatcher
from Bots.logger.logger import logger
from aiogram.fsm.storage.memory import MemoryStorage
from Bots.telegram.Engineer_Bot.handlers import keyboards_logic, auth
from Bots.telegram.Engineer_Bot.handlers.orders import agreement, prepayment, outlay_record, report, stationary
from Bots.telegram.Engineer_Bot.handlers.account import penalty
from Bots.telegram.asinc_requests.asinc_requests import refresh_access_tokens
from Bots.DB.sqlite_db import Db
from dotenv import load_dotenv
import os



async def create_db():
    db = Db()
    await db.create_users_table()

async def periodic_task():
    while True:
        logger.info(f'Engineer bot refresh_access_tokens')
        await refresh_access_tokens()
        await asyncio.sleep(20 * 60 * 60)

async def main():
    await create_db()
    dp = Dispatcher(storage=MemoryStorage())
    load_dotenv()
    bot = Bot(token=os.environ.get("ENGINEER_BOT_TOKEN"))
    dp.include_router(keyboards_logic.router)
    dp.include_router(auth.router)
    dp.include_router(agreement.router)
    dp.include_router(prepayment.router)
    dp.include_router(outlay_record.router)
    dp.include_router(report.router)
    dp.include_router(stationary.router)
    dp.include_router(penalty.router)
    logger.info(f'Engineer bot started')
    await asyncio.gather(
        dp.start_polling(bot),
        periodic_task()
    )



if __name__ == '__main__':
    asyncio.run(main())
