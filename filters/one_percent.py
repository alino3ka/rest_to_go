import random
import logging

from aiogram.filters import Filter
from aiogram.types import Message


class OnePercentDropFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        passed = random.randint(0, 99) > 0
        if not passed:
            logging.debug("message is unlucky")
        return passed
