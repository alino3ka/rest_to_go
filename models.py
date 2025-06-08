from collections import defaultdict
from dataclasses import dataclass

from aiogram.types import Message

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


class Languages:
    def __init__(self, known_langs: set[str]):
        self.langs: dict[int, str] = defaultdict(lambda: 'en')
        self.known_langs = known_langs

    @classmethod
    def load(cls, known_langs: set[str]):
        def reader(v):
            assert isinstance(v, dict)
            r = defaultdict(lambda: 'en')
            for k, l in v.items():
                assert l in known_langs
                r[int(k)] = l
            return r

        this = cls(known_langs)
        try:
            this.langs = storage.load("admin", "langs", reader)
        except FileNotFoundError:
            pass
        return this

    def store(self):
        storage.store("admin", "langs", dict(self.langs))

    def __getitem__(self, id_: int | Message) -> str:
        if isinstance(id_, Message):
            if id_.from_user is None:
                return "en"
            return self.langs[id_.from_user.id]
        return self.langs[id_]

    def __setitem__(self, id_: int, lang: str):
        if lang not in self.known_langs:
            raise ValueError("not known languange")
        self.langs[id_] = lang
        self.store()
