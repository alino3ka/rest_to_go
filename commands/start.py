from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Hello")
