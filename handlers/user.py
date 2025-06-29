import os
import hashlib, urllib.parse
from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.base import StorageKey
from handlers.texts import TEXTS
from aiogram.types import CallbackQuery
from keyboards.userkb import start_btn, pay_btn
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiohttp import web
from aiogram import Bot
from datetime import datetime, timedelta
from database.requests import set_user, save_info_user
from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
user = Router()
bot = Bot(token=BOT_TOKEN)


async def get_amount():
    return os.getenv("COST")


async def get_secret_key():
    return os.getenv("SECRET")


class Invite(StatesGroup):
    welcome = State()
    pay = State()
    success_pay = State()
    failed_pay = State()
    expire = State()


@user.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await set_user(message.from_user.id)
    await save_info_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    button = start_btn()
    await state.set_state(Invite.welcome)
    await message.answer(TEXTS.get("welcome"), reply_markup=button)


def generate_payment_link(
    amount: int, telegram_id: int, username: str,
        first_name: str, last_name: str, secret_key: str) -> str:
    base_url = "https://checkout.ckassa.com/pay"
    currency = "RUB"

    params = {
        "amount": str(amount),
        "currency": currency,
        f"meta[user_id]": str(telegram_id),
        f"meta[username]": username,
        f"meta[first_name]": first_name,
        f"meta[last_name]": last_name,
    }

    # Формируем строку для создания подписи
    to_sign = "".join([
        secret_key,
        params["amount"],
        params["currency"],
        params[f"meta[user_id]"]
        # + другие параметры по документации CKassa...
    ])

    sign = hashlib.md5(to_sign.encode('utf-8')).hexdigest()
    params["sign"] = sign

    return f"{base_url}?{urllib.parse.urlencode(params)}"


async def send_pay_prompt(
    user_id,
    bot: Bot,
    storage,
    text: str,
    keyboard,
    state_cls: State
):

    await bot.send_message(user_id, text, reply_markup=keyboard)
    key = StorageKey(bot_id=bot.id, chat_id=user_id, user_id=user_id)
    await storage.set_state(key, state_cls)


@user.callback_query(F.data == "welcome_btn", Invite.welcome)
async def send_invite_message(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    username = callback.from_user.username
    first_name = callback.from_user.first_name
    last_name = callback.from_user.last_name
    amount = await get_amount()
    secret_key = await get_secret_key()
    pay_link = generate_payment_link(
        amount, user_id, username, first_name, last_name, secret_key)
    await send_pay_prompt(
        user_id=user_id,
        bot=callback.bot,
        storage=state.storage,
        text=TEXTS.get("pay"),
        keyboard=pay_btn(user_id, pay_link, TEXTS.get("pay_btn")),
        state_cls=Invite.pay
    )
    await callback.answer()


async def generate_private_link():
    invite_link = await bot.create_chat_invite_link(
        chat_id=int(os.getenv("CHAT_ID")),
        member_limit=1,
        expire_date=int((datetime.now() + timedelta(hours=1)).timestamp()))
    return invite_link.invite_link
