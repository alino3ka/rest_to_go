from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message

from filters.night_hours import NotNightHours
from models import Languages
from utils.localize import localize

router = Router()

@router.message(CommandStart(), NotNightHours())
async def start_handler(message: Message, langs: Languages):
    await message.answer(localize("hello", message, langs))
