from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from create_bot import kb_list
from utils.db import get_user_by_id, add_user, update_bot_open_status
from keyboards.kb import main_contact_kb, channels_kb
from utils.utils import is_user_subscribed


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    telegram_id = message.from_user.id
    user_data = await get_user_by_id(telegram_id)

    if user_data is None:
        await add_user(
            telegram_id=telegram_id,
            username=message.from_user.id,
            first_name=message.from_user.first_name
        )
        bot_open = False
    else:
        bot_open = user_data.get('bot_open', False)

    if bot_open:
        await message.answer("Тут логика")
    else:
        await message.answer(
            "Для пользования ботом необходимо подписаться на следующие каналы:",
            reply_markup=channels_kb(kb_list)
        )