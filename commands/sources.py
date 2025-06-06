import dataclasses
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiohttp import ClientSession

from models import ListSources, Location
from services.nominatim import guess_name

router = Router()

class AddSource(StatesGroup):
    location = State()
    name = State()

@router.message(Command("add_source"))
async def add_source(message: Message, state: FSMContext):
    await state.set_state(AddSource.location)
    await message.answer("Send location of new source")

@router.message(AddSource.location, F.location)
async def add_location(message: Message, state: FSMContext, session: ClientSession):
    assert message.location
    lat = message.location.latitude
    lon = message.location.longitude
    name = await guess_name(session, lat, lon)
    await state.update_data(location=Location(name, lat, lon))
    await state.set_state(AddSource.name)
    await message.answer(
        "Enter name for source",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=name)],
            ],
            resize_keyboard=True,
        )
    )

@router.message(AddSource.location)
async def need_location(message: Message):
    await message.answer("Just send location")

@router.message(AddSource.name, F.text)
async def add_name(message: Message, state: FSMContext, sources: ListSources):
    data = await state.get_data()
    await state.clear()
    loc: Location = dataclasses.replace(data["location"], name=message.text)
    sources.append(loc)
    await message.answer(
        f"Saved new source, now I know {len(sources)} sources",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(AddSource.name)
async def need_name(message: Message):
    await message.answer("Send a name of location")

@router.message(Command("clear_sources"))
async def clear_sources(message: Message, sources: ListSources):
    sources.clear()
    await message.answer("Cleared all known sources")

@router.message(Command("sources"))
async def sources(message: Message, sources: ListSources):
    if not sources:
        await message.answer("No known sources")
        return
    locs = []
    for i, loc in enumerate(sources):
        locs.append(f"{i}: {loc.name} ({loc.lat}, {loc.lon})")
    await message.answer("\n".join(locs))
