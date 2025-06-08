import logging
from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from aiohttp.client import ClientResponseError


class CatchMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Any],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except (ValueError, ClientResponseError) as e:
            logging.error("exception occured with type %s: %s", type(e).__name__, e)
            if isinstance(event, Message):
                await event.answer("Something went wrong, sorry")
