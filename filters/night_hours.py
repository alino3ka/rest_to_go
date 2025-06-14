from aiogram.filters import Filter
from aiogram.types import Message


class NotNightHours(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.date.hour not in range(0, 5)
