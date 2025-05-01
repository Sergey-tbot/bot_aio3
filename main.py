import asyncio

from aiogram import Bot, Dispatcher
from data.config import Config, load_config
from handlers import private


async def main() -> None:
    config : Config = load_config()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    dp.include_router(private.router)

    await dp.start_polling(bot)


asyncio.run(main())