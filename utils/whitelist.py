from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from models import UserWhiteList


class WhiteListMiddleware(BaseMiddleware):
    def __init__(self, whitelist: UserWhiteList):
        self.whitelist = whitelist

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Any],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if isinstance(event, Message):
            sender = event.from_user
            if sender is not None and sender.id not in self.whitelist:
                return
        await handler(event, data)
