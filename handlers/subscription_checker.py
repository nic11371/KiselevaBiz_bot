import os
from asyncio import sleep
from datetime import datetime
from variables import PREV_LAST_DATE, LAST_DATE
from database.requests import get_all_users, update_status
from keyboards.userkb import pay_btn
from handlers.texts import TEXTS
from handlers.user import generate_payment_link


class BaseUser:
    def __init__(self, user_data):
        self.data = user_data
        self.now = datetime.utcnow()
        self.amount = int(os.getenv("COST", 0))
        self.secret_key = os.getenv("SECRET")
        self.chat_id = int(os.getenv("CHAT_ID", 0))

    def days_since_payment(self) -> int:
        if not self.data.last_pay_date:
            return -1
        return (self.now - self.data.last_pay_date).days

    def generate_pay_link(self) -> str:
        return generate_payment_link(
            amount=self.amount,
            telegram_id=self.data.tg_id,
            username=self.data.username,
            first_name=self.data.first_name,
            last_name=self.data.last_name,
            secret_key=self.secret_key
        )

    def generate_keyboard(self, pay_link: str):
        return pay_btn(self.data.tg_id, pay_link, TEXTS.get("pay_btn"))

    async def notify(self, bot, message: str, keyboard):
        await bot.send_message(self.data.tg_id, message, reply_markup=keyboard)

    async def process(self, bot):
        raise NotImplementedError


class StandardUser(BaseUser):
    async def process(self, bot):
        if not self.data.last_pay_date or not self.data.status_pay:
            return

        days = self.days_since_payment()
        pay_link = self.generate_pay_link()
        keyboard = self.generate_keyboard(pay_link)

        if days == int(PREV_LAST_DATE) and self.now.date() \
                != self.data.last_pay_date.date():
            await self.notify(bot, TEXTS.get("subscribe"), keyboard)
            print(f"[DEBUG] Напоминание отправлено: {self.data.tg_id}")

        elif days >= int(LAST_DATE):
            await update_status(self.data.tg_id, False)
            try:
                await bot.ban_chat_member(self.chat_id, self.data.tg_id)
                await bot.unban_chat_member(self.chat_id, self.data.tg_id)
            except Exception as e:
                print(f"[ERROR]: {self.data.tg_id}, ошибка: {e}")
            await self.notify(bot, TEXTS.get("unsubscribe"), keyboard)
            print(f"[DEBUG] Подписка отключена: {self.data.tg_id}")


class UserFactory:
    @staticmethod
    def create(user_data):
        # В будущем можно делать разные классы по user_data.role
        return StandardUser(user_data)


async def subscription_checker(bot):
    time_delay = int(os.getenv("TIME", 3600))

    while True:
        users = await get_all_users()
        for user_data in users:
            user = UserFactory.create(user_data)
            await user.process(bot)
        await sleep(time_delay)
