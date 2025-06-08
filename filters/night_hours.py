from aiogram.types import Message


def not_night_hours(self, message: Message) -> bool:
    return message.date.hour not in range(0, 5)
