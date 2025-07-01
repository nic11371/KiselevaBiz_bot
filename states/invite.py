from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.base import StorageKey


class Invite(StatesGroup):
    welcome = State()
    pay = State()
    success_pay = State()
    failed_pay = State()
    expire = State()


async def get_keys(bot, user_id):
    return StorageKey(bot_id=bot, chat_id=user_id, user_id=user_id)
