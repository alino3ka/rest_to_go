import json
from pathlib import Path
from typing import Any, Callable

from config import STORAGE_PATH

root = Path(STORAGE_PATH)


def load[T](prefix: str, name: str, reader: Callable[[Any], T]) -> T:
    dir = root / prefix
    dir.mkdir(parents=True, exist_ok=True)
    with (dir / name).open() as f:
        value = json.load(f)
    return reader(value)

def store(prefix: str, name: str, value: Any):
    dir = root / prefix
    dir.mkdir(parents=True, exist_ok=True)
    with (dir / name).open("w") as f:
        json.dump(value, f)
