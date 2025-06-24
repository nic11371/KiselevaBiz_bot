from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from handlers.texts import TEXTS
from aiogram.types import CallbackQuery
from keyboards.userkb import start_btn, pay_btn
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiohttp import web


user = Router()


class Invite(StatesGroup):
    welcome = State()
    pay = State()
    success_pay = State()
    failed_pay = State()
    expire = State()


@user.message(CommandStart())
async def start(message: Message, state: FSMContext):
    button = start_btn()
    await message.answer(TEXTS.get("welcome"), reply_markup=button)
    await state.set_state(Invite.welcome)


@user.callback_query(F.data == "welcome_btn", Invite.welcome)
async def send_invite_message(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(TEXTS.get("pay"), reply_markup=pay_btn())
    await state.set_state(Invite.pay)
    await callback.answer()


@user.callback_query(F.data == "pay_btn", Invite.pay)
async def send_pay_message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()


# async def payment_webhook(request: web.Request):
#     data = await request.json()
#     user_id = data.get("custom_fields", {}).get("telegram_id")
#     payment_status = data.get("status")

#     if payment_status == "success":
#         # Здесь вы должны отправить сообщение через bot.send_message
#         from bot import bot  # Импорт из основного файла, где инициализирован bot
#         await bot.send_message(chat_id=user_id, text=TEXTS.get("payment_success"))
#     elif payment_status == "fail":
#         await bot.send_message(chat_id=user_id, text=TEXTS.get("payment_failed"))

#     return web.Response(text="OK")