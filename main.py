import asyncio

from bot import dp, bot
from handlers import group, private, private_admin
from aiogram.types import Update

import json


dp.include_router(group.router)
dp.include_router(private_admin.router)
dp.include_router(private.router)




# Yandex.Cloud functions handler.
async def process_event(event):
    update = json.loads(event['body'])
    update = Update.model_validate(update)
    await dp.feed_update(bot=bot, update=update)


async def handler(event, context):
    await process_event(event)
    # await process_event(update)
    return {
        'statusCode': 200,
        'body': 'ok',
    }


async def main() -> None:
    await dp.start_polling(bot)

asyncio.run(main())