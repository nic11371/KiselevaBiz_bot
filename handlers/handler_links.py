import hashlib
import urllib.parse
from states.invite import get_keys
from variables import DOMAIN_PAY, CURRENCY, COST, SECRET
from aiogram import Bot
from aiogram.fsm.state import State


async def get_amount():
    return COST


async def get_secret_key():
    return SECRET


def generate_payment_link(
    amount: int, telegram_id: int, username: str,
        first_name: str, last_name: str, secret_key: str) -> str:
    base_url = DOMAIN_PAY
    currency = CURRENCY

    params = {
        "amount": str(amount),
        "currency": currency,
        "meta[user_id]": str(telegram_id),
        "meta[username]": username,
        "meta[first_name]": first_name,
        "meta[last_name]": last_name,
    }

    # Формируем строку для создания подписи
    to_sign = "".join([
        secret_key,
        params["amount"],
        params["currency"],
        params["meta[user_id]"]
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
    key = await get_keys(bot.id, user_id)
    await storage.set_state(key, state_cls)
