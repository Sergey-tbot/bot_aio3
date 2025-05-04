import asyncio
from bot import dp, bot
from handlers import group, private, private_admin

async def main() -> None:
    dp.include_router(group.router)
    dp.include_router(private_admin.router)
    dp.include_router(private.router)

    await dp.start_polling(bot)

asyncio.run(main())