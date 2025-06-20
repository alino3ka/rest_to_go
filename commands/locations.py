import dataclasses
import logging
from typing import Iterator

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiohttp import ClientSession

from models import DestinationList, SourceList, Location
from services.nominatim import guess_name

router = Router()

class AddLocation(StatesGroup):
    location = State()
    name = State()

@router.message(Command("add_source"))
async def add_source_handler(message: Message, state: FSMContext):
    await state.update_data(is_source=True)
    await state.set_state(AddLocation.location)
    await message.answer("Send location of new source")

@router.message(Command("add_destination"))
async def add_destination_handler(message: Message, state: FSMContext):
    await state.update_data(is_source=False)
    await state.set_state(AddLocation.location)
    await message.answer("Send location of new destination")

@router.message(AddLocation.location, F.location)
async def add_location_handler(message: Message, state: FSMContext, session: ClientSession):
    assert message.location
    lat = message.location.latitude
    lon = message.location.longitude
    name = await guess_name(session, lat, lon)
    await state.update_data(location=Location(name, lat, lon))
    await state.set_state(AddLocation.name)
    await message.answer(
        "Enter name for location",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=name)],
            ],
            resize_keyboard=True,
        )
    )

@router.message(AddLocation.location)
async def need_location_handler(message: Message):
    await message.answer("Just send location")

@router.message(AddLocation.name, F.text)
async def add_name_handler(
    message: Message,
    state: FSMContext,
    sources: SourceList,
    destinations: DestinationList,
):
    data = await state.get_data()
    await state.clear()
    loc: Location = dataclasses.replace(data["location"], name=message.text)
    if data["is_source"]:
        sources.append(loc)
        await message.answer(
            f"Saved new source, now I know {len(sources)} sources",
            reply_markup=ReplyKeyboardRemove(),
        )
        logging.debug("Added new source")
    else:
        destinations.append(loc)
        await message.answer(
            f"Saved new destination, now I know {len(destinations)} destinations",
            reply_markup=ReplyKeyboardRemove(),
        )
        logging.debug("Added new destination")

@router.message(AddLocation.name)
async def need_name_handler(message: Message):
    await message.answer("Send a name of location")

@router.message(Command("clear_sources"))
async def clear_sources_handler(message: Message, sources: SourceList):
    sources.clear()
    await message.answer("Cleared all known sources")
    logging.debug("Cleared sources")

@router.message(Command("clear_destinations"))
async def clear_destinations_handler(message: Message, destinations: DestinationList):
    destinations.clear()
    await message.answer("Cleared all known destinations")
    logging.debug("Cleared destinations")

@router.message(Command("sources"))
async def sources_handler(message: Message, sources: SourceList):
    if not sources:
        await message.answer("No known sources")
        return
    await message.answer(_format_locations(iter(sources)))

@router.message(Command("destinations"))
async def destinations_handler(message: Message, destinations: DestinationList):
    if not destinations:
        await message.answer("No known destinations")
        return
    await message.answer(_format_locations(iter(destinations)))

def _format_locations(locs: Iterator[Location]) -> str:
    parts: list[str] = []
    for i, loc in enumerate(locs, 1):
        parts.append(f"{i}: {loc.pretty()}")
    return "\n".join(parts)
