from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from keyboards import keyboard

router= Router()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Start')

@router.message()
async def send_echo(message: Message):

    try:
        await message.send_copy(chat_id=message.chat.id, reply_markup=keyboard.keyboard_private)
    except TypeError:
        await message.reply(text='no echo')