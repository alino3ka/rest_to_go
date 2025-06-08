import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.methods import SetMyCommands
from aiogram.types import BotCommand, Message, ReplyKeyboardRemove
from aiohttp.client import ClientSession

from config import BOT_TOKEN, INITIAL_USER_ID
from commands import admin, start, locations, matrix
from middlewares.exceptions import CatchMiddleware
from middlewares.whitelist import WhiteListMiddleware
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
    BotCommand(command="/matrix", description="Calculate matrix distance"),
    BotCommand(command="/best", description="Find best destination from all sources"),
    BotCommand(command="/add_user", description="Add user to whitelist"),
    BotCommand(command="/remove_user", description="Remove user from whitelist"),
]

last_router = Router()

@last_router.message()
async def unknown_handler(message: Message):
    await message.answer("I don't know what you want")

WHITELIST = models.UserWhiteList.load()
WHITELIST.add(int(INITIAL_USER_ID))

dp = Dispatcher()
dp.include_routers(
    admin.router,
    start.router,
    locations.router,
    matrix.router,
    last_router,
)
dp.message.middleware(CatchMiddleware())
dp.message.middleware(WhiteListMiddleware(WHITELIST))


@dp.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Operation canceled",
        reply_markup=ReplyKeyboardRemove(),
    )

async def main():
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
            whitelist=WHITELIST,
        )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
