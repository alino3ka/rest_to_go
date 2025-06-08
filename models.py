from dataclasses import dataclass

import storage

@dataclass(frozen=True)
class Location:
    name: str
    lat: float
    lon: float

    def pretty(self) -> str:
        return f"{self.name} ({self.lat}, {self.lon})"

class LocationList:
    def __init__(self):
        self.locs: list[Location] = []

    def append(self, loc: Location):
        self.locs.append(loc)

    def clear(self):
        self.locs.clear()

    def __bool__(self):
        return bool(self.locs)

    def __iter__(self):
        return iter(self.locs)

    def __len__(self):
        return len(self.locs)

    def __getitem__(self, i: int) -> Location:
        return self.locs[i]


class SourceList(LocationList):
    pass


class DestinationList(LocationList):
    pass


class UserWhiteList:
    def __init__(self):
        self.whitelist: set[int] = set()

    @classmethod
    def load(cls):
        def reader(v):
            assert isinstance(v, list)
            assert all(isinstance(e, int) for e in v)
            return set(v)

        try:
            whitelist = storage.load("admin", "whitelist", reader)
        except FileNotFoundError:
            whitelist = set()

        this = cls()
        this.whitelist = whitelist
        return this

    def store(self):
        storage.store("admin", "whitelist", list(self.whitelist))

    def add(self, id_: int):
        self.whitelist.add(id_)
        self.store()

    def remove(self, id_: int):
        self.whitelist.discard(id_)
        self.store()

    def __contains__(self, id_: int) -> bool:
        return id_ in self.whitelist

    def __len__(self) -> int:
        return len(self.whitelist)
