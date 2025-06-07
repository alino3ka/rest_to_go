from dataclasses import dataclass

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
