from asyncio import sleep
from database.requests import get_all_users, update_status
from datetime import datetime
from keyboards.userkb import pay_btn
from handlers.texts import TEXTS
from handlers.user import generate_payment_link
import os


async def subscription_checker(bot):
    amount = os.getenv("COST")
    secret_key = os.getenv("SECRET")
    chat_id = int(os.getenv("CHAT_ID"))
    time_delay = int(os.getenv("TIME"))

    while True:
        users = await get_all_users()
        now = datetime.utcnow()

        for u in users:
            if u.last_pay_date is None:
                continue
            delta = now - u.last_pay_date

            pay_link = generate_payment_link(
                amount=int(amount),
                telegram_id=u.tg_id,
                username=u.username,
                first_name=u.first_name,
                last_name=u.last_name,
                secret_key=secret_key
            )

            keyboard = pay_btn(u.tg_id, pay_link, TEXTS.get("pay_btn"))

            if delta.days == 29 and u.status_pay:
                if not u.last_pay_date or (
                        now.date() != u.last_pay_date.date()):
                    await bot.send_message(
                        u.tg_id, TEXTS.get("subscribe"), reply_markup=keyboard)
                    print(f"[DEBUG] Отправлено сообщение пользователю {u.tg_id}")

            if delta.days >= 30 and u.status_pay:
                print(f"[DEBUG] Ставим статус False для {u.tg_id}")
                await update_status(u.tg_id, False)
                try:
                    await bot.ban_chat_member(
                        chat_id=chat_id, user_id=u.tg_id)
                    await bot.unban_chat_member(
                        chat_id=chat_id, user_id=u.tg_id)
                except Exception as e:
                    print(f"Ошибка при удалении из чата {u.tg_id}: {e}")
                await bot.send_message(
                    u.tg_id, TEXTS.get("unsubscribe"), reply_markup=keyboard)

        await sleep(time_delay)
