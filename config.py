import os

file_kv: dict[str, str] = {}
with open(".env") as f:
    for line in f:
        key, value = line.strip().split("=", 1)
        file_kv[key] = value

def _get(name: str) -> str:
    value = os.environ.get(name)
    if value is None:
        value = file_kv.get(name)
    if value is None:
        raise ValueError(f"not found key: {key}")
    return value

BOT_TOKEN = _get("BOT_TOKEN")
OPENROUTESERVICE_TOKEN = _get("OPENROUTESERVICE_TOKEN")
STORAGE_PATH = _get("STORAGE_PATH")
INITIAL_USER_ID = _get("INITIAL_USER_ID")
LOG_LEVEL = _get("LOG_LEVEL")
