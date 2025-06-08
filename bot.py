import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.methods import DeleteMyCommands, SetMyCommands
from aiogram.types import BotCommand, Message, ReplyKeyboardRemove
from aiohttp.client import ClientSession, ClientTimeout

from config import BOT_TOKEN, INITIAL_USER_ID, LOG_LEVEL
from commands import admin, start, lang, locations, matrix
from middlewares.exceptions import CatchMiddleware
from middlewares.whitelist import WhiteListMiddleware
import models
from utils import localize

COMMANDS = [
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
    BotCommand(command="/stats", description="Statistics of bot"),
    BotCommand(command="/help", description="Show help text"),
    BotCommand(command="/cancel", description="Cancel current operation"),
    BotCommand(command="/language_ru", description="Set russian language"),
    BotCommand(command="/language_en", description="Set english language"),
]

last_router = Router()

@last_router.message()
async def unknown_handler(message: Message):
    await message.answer("I don't know what you want")


dp = Dispatcher()
dp.include_routers(
    admin.router,
    start.router,
    lang.router,
    locations.router,
    matrix.router,
    last_router,
)
dp.message.middleware(CatchMiddleware())


@dp.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Operation canceled",
        reply_markup=ReplyKeyboardRemove(),
    )

@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("This bot helps to find the place that minimize road time from all sources")

async def main():
    whitelist = models.UserWhiteList.load()
    whitelist.add(int(INITIAL_USER_ID))
    dp.message.middleware(WhiteListMiddleware(whitelist))

    langs = models.Languages.load(set(localize.locales.keys()))

    bot = Bot(token=BOT_TOKEN)
    await bot(DeleteMyCommands())
    await bot(SetMyCommands(commands=COMMANDS))
    headers = {
        "User-Agent": "rest_to_go",
    }
    sources = models.SourceList()
    destinations = models.DestinationList()
    timeout = ClientTimeout(total=60)
    async with ClientSession(headers=headers, timeout=timeout, raise_for_status=True) as session:
        await dp.start_polling(
            bot,
            session=session,
            sources=sources,
            destinations=destinations,
            whitelist=whitelist,
            langs=langs,
        )

if __name__ == "__main__":
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARN": logging.WARN,
        "ERROR": logging.ERROR,
    }
    logging.basicConfig(level=log_levels[LOG_LEVEL], stream=sys.stdout)
    asyncio.run(main())
