import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.api import bot_router
from src.bll.question import questions_loader
from src.core.db.init import init_db
from src.core.logging_config import setup_logging
from src.core.middlewares.db import DatabaseMiddleware
from src.core.settings import config

setup_logging()


async def main() -> None:
    questions_loader.load()
    await init_db()

    dp: Dispatcher = Dispatcher()
    dp.message.middleware.register(DatabaseMiddleware())
    dp.include_router(bot_router)

    bot: Bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
