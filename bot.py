import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiohttp.client import ClientSession

from config import BOT_TOKEN
from services.nominatim import guess_name

dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: Message):
    sender = message.from_user
    if sender is None:
        await message.answer("Hello, anonymous!")
    else:
        await message.answer(f"Hello, {sender.full_name}")

@dp.message(F.location)
async def guess_name_handler(message: Message):
    assert message.location
    async with ClientSession() as sess:
        name = await guess_name(sess, message.location.latitude, message.location.longitude)
    await message.answer(name)

async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
