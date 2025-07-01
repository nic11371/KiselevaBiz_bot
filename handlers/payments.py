from aiohttp import web
from handlers.texts import TEXTS
from states.invite import get_keys
from handlers.user import send_pay_prompt, generate_private_link, \
    generate_payment_link, Invite
from keyboards.userkb import pay_btn
from database.requests import get_user, update_status
from handlers.user import get_amount, get_secret_key


class PaymentHandler:
    def __init__(self, bot, storage):
        self.bot = bot
        self.storage = storage

    async def handle(self, data):
        status = data.get("status", "").lower()
        meta = data.get("meta", {})
        user_id = meta.get("user_id")
        if not user_id:
            return web.Response(status=400, text="user_id not found")

        self.meta = meta
        self.user_id = user_id
        self.key = await get_keys(self.bot.id, user_id)
        self.amount = await get_amount()
        self.secret_key = await get_secret_key()
        self.pay_link = generate_payment_link(
            self.amount, user_id, meta.get("username"),
            meta.get("first_name"), meta.get("last_name"),
            self.secret_key
        )

        handler = self.status_dispatcher().get(status, self.handle_unknown)
        return await handler()

    def status_dispatcher(self):
        return {
            "payed": self.handle_payed,
            "processed": self.handle_payed,
            "created_error": self.handle_failed,
            "rejected": self.handle_failed,
            "refunded": self.handle_failed,
            "error": self.handle_failed,
        }

    async def handle_payed(self):
        old_user = await get_user(self.user_id)
        old_status = old_user.status_pay if old_user else False
        await update_status(self.user_id, True)
        await self.storage.set_state(self.key, Invite.success_pay)

        if old_status:
            await self.bot.send_message(self.user_id, TEXTS.get("already_pay"))
        else:
            link = await generate_private_link()
            await self.bot.send_message(
                self.user_id,
                TEXTS.get("success_pay").format(link=link)
            )
        return web.Response(text="OK")

    async def handle_failed(self):
        await send_pay_prompt(
            user_id=self.user_id,
            bot=self.bot,
            storage=self.storage,
            text=TEXTS.get("unsuccess_pay"),
            keyboard=pay_btn(
                self.user_id, self.pay_link, TEXTS.get("unsuccess_pay_btn")
            ),
            state_cls=Invite.pay
        )
        return web.Response(text="OK")

    async def handle_unknown(self):
        await self.bot.send_message(
            self.user_id, f"ℹ️ Статус платежа: {self.meta.get('status')}")
        return web.Response(text="OK")
