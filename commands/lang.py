from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from models import Languages
from utils.localize import localize


router = Router()

@router.message(Command("language_ru"))
async def language_ru_handler(
    message: Message,
    langs: Languages,
):
    sender = message.from_user
    if sender is None:
        return
    langs[sender.id] = "ru"
    await message.answer(localize("lang_updated", message, langs, lang="ru"))

@router.message(Command("language_en"))
async def language_en_handler(
    message: Message,
    langs: Languages,
):
    sender = message.from_user
    if sender is None:
        return
    langs[sender.id] = "en"
    await message.answer(localize("lang_updated", message, langs, lang="en"))
