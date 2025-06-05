import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import BOT_TOKEN

dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: Message):
    sender = message.from_user
    if sender is None:
        await message.answer("Hello, anonymous!")
    else:
        await message.answer(f"Hello, {sender.full_name}")

async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
