import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from Bots.telegram.SuperUser_Bot.handlers import auth, create_tutor, get_tutors, delete_tutor
from Bots.DB.sqlite_db import Db
from Bots.logger.logger import logger
from dotenv import load_dotenv
from Bots.telegram.asinc_requests.asinc_requests import refresh_access_tokens
import os



async def create_db():
    db = Db()
    await db.create_users_table()

async def periodic_task():
    while True:
        logger.info(f'SuperUser bot refresh_access_tokens')
        await refresh_access_tokens()
        await asyncio.sleep(20 * 60 * 60)


async def main():
    await create_db()
    dp = Dispatcher(storage=MemoryStorage())
    load_dotenv()
    bot = Bot(token=os.environ.get("SUPER_USER_BOT_TOKEN"))
    dp.include_router(auth.router)
    dp.include_router(create_tutor.router)
    dp.include_router(get_tutors.router)
    dp.include_router(delete_tutor.router)
    logger.info(f'SuperUser bot started')
    await asyncio.gather(
        dp.start_polling(bot),
        periodic_task()
    )


if __name__ == '__main__':
    asyncio.run(main())
