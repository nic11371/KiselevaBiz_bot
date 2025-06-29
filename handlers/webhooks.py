from aiogram import Bot
from datetime import datetime, timedelta
from aiohttp import web
from handlers.texts import TEXTS
from aiogram.fsm.storage.base import StorageKey
from handlers.user import send_pay_prompt, generate_private_link, \
    generate_payment_link, Invite
from keyboards.userkb import pay_btn
from database.requests import get_user, set_user, save_info_user, update_status
from handlers.user import get_amount, get_secret_key


async def ckassa_webhook(request, bot, storage):
    amount = await get_amount()
    secret_key = await get_secret_key()
    data = await request.json()
    status = data.get("status", "").lower()
    meta = data.get("meta", {})
    user_id = meta.get("user_id")
    user_username = meta.get("username")
    user_first_name = meta.get("first_name")
    user_last_name = meta.get("last_name")
    print("📦 Meta from CKassa:", meta)

    if not user_id:
        return web.Response(status=400, text="user_id not found")

    key = StorageKey(bot_id=bot.id, chat_id=user_id, user_id=user_id)
    pay_link = generate_payment_link(
        amount, user_id, user_username,
        user_first_name, user_last_name, secret_key)

    if status in ["payed", "processed"]:
        # 1. Получаем состояние перед изменением
        old_user = await get_user(user_id)
        old_status = old_user.status_pay if old_user else False

        # 2. Обновляем данные
        await set_user(user_id)
        await save_info_user(
            user_id, user_username, user_first_name, user_last_name)
        await update_status(user_id, True)

        # 3. Определяем, что делать
        if old_status:
            await bot.send_message(user_id, TEXTS.get("already_pay"))
        else:
            # первая оплата
            await storage.set_state(key, Invite.success_pay)
            private_link = await generate_private_link()
            await bot.send_message(
                user_id, TEXTS.get("success_pay").format(link=private_link))
    elif status in ["created_error", "rejected", "refunded", "error"]:
        await send_pay_prompt(
            user_id=user_id,
            bot=bot,
            storage=storage,
            text=TEXTS.get("unsuccess_pay"),
            keyboard=pay_btn(
                user_id, pay_link, TEXTS.get("unsuccess_pay_btn")),
            state_cls=Invite.pay
        )
    else:
        await bot.send_message(user_id, f"ℹ️ Статус платежа: {status}")

    return web.Response(text="OK")
