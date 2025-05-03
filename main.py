import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from data.config_bot import Config, load_config
from aiogram.client.default import DefaultBotProperties
from handlers import private, group, private_admin


async def main() -> None:
    config : Config = load_config()

    bot = Bot(token=config.tg_bot.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(group.router)
    dp.include_router(private_admin.router)
    dp.include_router(private.router)

    await dp.start_polling(bot)

asyncio.run(main())