import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.methods import SetMyCommands
from aiogram.types import BotCommand, Message
from aiohttp.client import ClientSession

from config import BOT_TOKEN
from commands import admin, start, locations, matrix
import models

COMMANDS = [
    BotCommand(command="/cancel", description="Cancel current operation"),
    BotCommand(command="/stats", description="Statistics of bot"),
    BotCommand(command="/add_source", description="Add a new source"),
    BotCommand(command="/add_destination", description="Add a new destination"),
    BotCommand(command="/sources", description="List all sources"),
    BotCommand(command="/destinations", description="List all destinations"),
    BotCommand(command="/clear_sources", description="Clear all known sources"),
    BotCommand(command="/clear_destinations", description="Clear all known destinations"),
    BotCommand(command="/matrix", description="Calculate matrix distance")
]

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
        matrix.router,
        last_router,
    )


    bot = Bot(token=BOT_TOKEN)
    await bot(SetMyCommands(commands=COMMANDS))
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
