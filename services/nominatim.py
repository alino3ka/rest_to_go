import logging
from datetime import timedelta
from functools import partial

from aiohttp import ClientSession

from utils.cache import Cache
from utils.throttler import Throttler

# See https://operations.osmfoundation.org/policies/nominatim/
THROTTLER = Throttler(timedelta(seconds=1))

CACHE: Cache[tuple[float, float], str] = Cache(100)

BASE_URL = "https://nominatim.openstreetmap.org/reverse"
DEFAULT_PARAMS = {
    "format": "jsonv2",
    "layer": "address,natural"
}

async def _guess_name(session: ClientSession, latlon: tuple[float, float]) -> str:
    lat, lon = latlon
    params = {"lat": lat, "lon": lon, **DEFAULT_PARAMS}
    async with THROTTLER:
        logging.debug("send guess name request at (%f, %f)", lat, lon)
        async with session.get(BASE_URL, params=params) as resp:
            response = await resp.json()
    return response["name"] or response["display_name"]

async def guess_name(session: ClientSession, lat: float, lon: float) -> str:
    return await CACHE.get_or_compute((lat, lon), partial(_guess_name, session))
