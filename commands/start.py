from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message

from filters.night_hours import not_night_hours

router = Router()

@router.message(CommandStart(), not_night_hours)
async def start_handler(message: Message):
    await message.answer("Hello")
