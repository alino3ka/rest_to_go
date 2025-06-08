import json
from pathlib import Path

from aiogram.types import Message

from models import Languages

locales: dict[str, dict[str, str]] = {}

locals_root = Path(__file__).parent.parent / "locales"
for locale in locals_root.iterdir():
    assert locale.is_file()
    assert locale.name.endswith(".json")
    name = locale.name[:-len(".json")]
    with locale.open() as f:
        locales[name] = json.load(f)


def localize(
    ident: str,
    message: Message,
    langs: Languages,
    **params: str,
) -> str:
    return locales[langs[message]][ident].format(**params)
