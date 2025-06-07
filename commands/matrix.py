from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import ClientSession

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
