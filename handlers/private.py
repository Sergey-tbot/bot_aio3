from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

router= Router()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Start')

@router.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='no echo')