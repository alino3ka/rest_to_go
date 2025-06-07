import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiohttp.client import ClientSession

from config import BOT_TOKEN
from commands import admin, start, locations
import models

async def unknown(message: Message):
    await message.answer("I don't know what you want")

async def main():
    last_router = Router()
    last_router.message()(unknown)

    dp = Dispatcher()
    dp.include_routers(
        admin.router,
        start.router,
        locations.router,
        last_router,
    )


    bot = Bot(token=BOT_TOKEN)
    headers = {
        "User-Agent": "rest_to_go",
    }
    sources = models.SourceList()
    destinations = models.DestinationList()
    async with ClientSession(headers=headers) as session:
        await dp.start_polling(
            bot,
            session=session,
            sources=sources,
            destinations=destinations,
        )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
