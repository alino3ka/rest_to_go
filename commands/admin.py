from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from models import DestinationList, SourceList, UserWhiteList

router = Router()

@router.message(Command("stats"))
async def stats_handler(
    message: Message,
    sources: SourceList,
    destinations: DestinationList,
    whitelist: UserWhiteList,
):
    lines = [
        f"Sources: {len(sources)}",
        f"Destinations: {len(destinations)}",
        f"Users: {len(whitelist)}",
    ]
    await message.answer("\n".join(lines))


class WhiteListManagement(StatesGroup):
    user_id = State()


@router.message(Command("add_user"))
async def add_user_handler(
    message: Message,
    state: FSMContext,
):
    await state.update_data(is_add=True)
    await state.set_state(WhiteListManagement.user_id)
    await message.answer("Send user id (you can find it using @userinfobot)")

@router.message(Command("remove_user"))
async def remove_user_handler(
    message: Message,
    state: FSMContext,
):
    await state.update_data(is_add=False)
    await state.set_state(WhiteListManagement.user_id)
    await message.answer("Send user id (you can find it using @userinfobot)")

@router.message(WhiteListManagement.user_id, F.text)
async def user_id_handler(
    message: Message,
    state: FSMContext,
    whitelist: UserWhiteList,
):
    assert message.text
    try:
        user_id = int(message.text)
    except ValueError:
        await message.answer("It isn't valid user id")
        return
    data = await state.get_data()
    await state.clear()
    if data["is_add"]:
        whitelist.add(user_id)
    else:
        whitelist.remove(user_id)
    await message.answer("Whitelist modified")


@router.message(WhiteListManagement.user_id)
async def need_user_id(message: Message):
    await message.answer("Just send user id")
