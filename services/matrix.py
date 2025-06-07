from datetime import timedelta

from aiohttp import ClientSession

from config import OPENROUTESERVICE_TOKEN
from models import DestinationList, SourceList
from utils.throttler import Throttler

THROTTLER = Throttler(timedelta(seconds=2))

BASE_URL = "https://api.openrouteservice.org/v2/matrix/driving-car"
HEADERS = {
    "Authorization": OPENROUTESERVICE_TOKEN,
}

async def calculate_matrix(
    session: ClientSession,
    sources: SourceList,
    destinations: DestinationList,
) -> list[list[float | None]]:
    locations = []
    for source in sources:
        locations.append([source.lon, source.lat])
    for destination in destinations:
        locations.append([destination.lon, destination.lat])
    data = {
        "locations": locations,
        "sources": list(range(len(sources))),
        "destinations": list(range(len(sources), len(locations))),
        "resolve_locations": False,
        "metrics": ["duration"],
    }
    async with session.post(BASE_URL, headers=HEADERS, json=data) as resp:
        resp.raise_for_status()
        durations = (await resp.json())["durations"]
    return durations
