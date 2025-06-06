import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiohttp.client import ClientSession

from config import BOT_TOKEN
from commands import start
from services.nominatim import guess_name

dp = Dispatcher()
dp.include_routers(
    start.router,
)

@dp.message(F.location)
async def guess_name_handler(message: Message, session: ClientSession):
    assert message.location
    name = await guess_name(session, message.location.latitude, message.location.longitude)
    await message.answer(name)

async def main():
    bot = Bot(token=BOT_TOKEN)
    headers = {
        "User-Agent": "rest_to_go",
    }
    async with ClientSession(headers=headers) as session:
        await dp.start_polling(bot, session=session)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
