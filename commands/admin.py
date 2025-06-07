from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from models import DestinationList, SourceList

router = Router()

@router.message(Command("stats"))
async def stats_handler(message: Message, sources: SourceList, destinations: DestinationList):
    await message.answer(f"Sources: {len(sources)}\nDestinations: {len(destinations)}")
