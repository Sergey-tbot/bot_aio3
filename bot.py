from aiogram import Bot, Dispatcher
from data.cfg import API_TOKEN
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

bot = Bot(token=API_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()