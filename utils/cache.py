from collections import OrderedDict
from typing import Awaitable, Callable


class Cache[K, V]:
    def __init__(self, maxsize: int):
        self.cache: OrderedDict[K, V] = OrderedDict()
        self.maxsize = maxsize

    def __getitem__(self, key: K):
        return self.cache[key]

    async def get_or_compute(self, key: K, compute: Callable[[K], Awaitable[V]]) -> V:
        v = self.cache.get(key)
        if v is None:
            if len(self.cache) == self.maxsize:
                self.cache.popitem(last=False)
            v = self.cache[key] = await compute(key)
        return v
