from datetime import timedelta

from aiohttp import ClientSession

from utils.throttler import Throttler

# See https://operations.osmfoundation.org/policies/nominatim/
THROTTLER = Throttler(timedelta(seconds=1))

BASE_URL = "https://nominatim.openstreetmap.org/reverse"
HEADERS = {
    "User-Agent": "rest_to_go",
}
DEFAULT_PARAMS = {
    "format": "jsonv2",
    "layer": "address,natural"
}

async def guess_name(sess: ClientSession, lat: float, lon: float) -> str:
    params = {"lat": lat, "lon": lon, **DEFAULT_PARAMS}
    async with THROTTLER:
        async with sess.get(BASE_URL, params=params, headers=HEADERS) as resp:
            response = await resp.json()
    return response["name"] or response["display_name"]
