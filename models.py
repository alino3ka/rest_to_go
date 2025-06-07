from dataclasses import dataclass

@dataclass(frozen=True)
class Location:
    name: str
    lat: float
    lon: float

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


class SourceList(LocationList):
    pass


class DestinationList(LocationList):
    pass
