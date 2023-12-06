import logging
import sys

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram import Bot, Dispatcher

from .config import POSTGRES_DB_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_ADMIN_ID

from .middlewares import DbSessionMiddleware

from .router import router

async def on_startup(bot: Bot) -> None:
    await bot.send_message(chat_id=TELEGRAM_ADMIN_ID, text="Bot started")

async def on_shutdown(bot: Bot) -> None:
    await bot.send_message(chat_id=TELEGRAM_ADMIN_ID, text="Bot is shutting down")
    await bot.session.close()


async def main() -> None:
    print("Bot is starting...")

    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",)

    engine = create_async_engine(POSTGRES_DB_URL, echo=True, connect_args={"options": "-c timezone=utc"})
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    
    bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode="HTML")
    
    dp = Dispatcher()
    dp.include_router(router)
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    
    try:
        aiohttp_logger = logging.getLogger("aiohttp.access")
        aiohttp_logger.setLevel(logging.INFO)
        
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        
        
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    
    except Exception as e:
        logging.exception(e)
        sys.exit(1)



if __name__ == "__main__":
    asyncio.run(main())
    