import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import ClientSession

from filters.one_percent import OnePercentDropFilter
from models import DestinationList, SourceList
from services.matrix import calculate_matrix

router = Router()

@router.message(Command("matrix"))
async def matrix_handler(
    message: Message,
    sources: SourceList,
    destinations: DestinationList,
    session: ClientSession,
):
    matrix = await calculate_matrix(session, sources, destinations)

    lines = []
    assert len(matrix) == len(sources)
    for durations, source in zip(matrix, sources):
        assert len(durations) == len(destinations)
        lines.append(source.pretty())
        for duration, destination in zip(durations, destinations):
            lines.append(f"> {destination.pretty()}: {duration if duration is not None else "Unknown"}")
    await message.answer("\n".join(lines))
    logging.debug("Calculated time matrix")


@router.message(Command("best"), OnePercentDropFilter())
async def best_handler(
    message: Message,
    sources: SourceList,
    destinations: DestinationList,
    session: ClientSession,
):
    matrix = await calculate_matrix(session, sources, destinations)

    best_i = -1
    best_dist = float('inf')
    for i in range(len(destinations)):
        dist = float('-inf')
        is_failed = False
        for row in matrix:
            v = row[i]
            if v is None:
                is_failed = True
                break
            dist = max(dist, v)
        if is_failed:
            continue
        if dist < best_dist:
            best_dist = dist
            best_i = i

    if best_i == -1:
        await message.answer("Sorry, I can't find good destination")
        logging.debug("Failed calculate best destination")
    else:
        await message.answer(f"Best is {destinations[best_i].pretty()}, {best_dist}")
        logging.debug("Calculated best destination")
