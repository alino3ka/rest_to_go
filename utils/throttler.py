import asyncio
from datetime import datetime, timedelta, timezone

TZ = timezone.utc


class Throttler:
    """Lock with maximum 1 acquire per `period`"""

    def __init__(self, period: timedelta):
        self.period = period
        self.lock = asyncio.Lock()
        self.last_call = datetime.fromtimestamp(0, TZ)

    async def __aenter__(self):
        await self.lock.acquire()
        now = datetime.now(TZ)
        if now - self.last_call < self.period:
            await asyncio.sleep((now - self.last_call).total_seconds())

    async def __aexit__(self, _exc_type, _exc, _tb):
        self.last_call = datetime.now(TZ)
        self.lock.release()
