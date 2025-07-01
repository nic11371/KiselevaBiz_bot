from datetime import datetime, timedelta
from aiogram import Bot
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from variables import BOT_TOKEN, CHAT_ID
from states.invite import Invite
from handlers.handler_links import get_amount, get_secret_key, \
    generate_payment_link, send_pay_prompt
from handlers.texts import TEXTS
from keyboards.userkb import start_btn, pay_btn
from database.requests import set_user, save_info_user


user = Router()
bot = Bot(token=BOT_TOKEN)


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
        chat_id=CHAT_ID,
        member_limit=1,
        expire_date=int((datetime.now() + timedelta(hours=1)).timestamp()))
    return invite_link.invite_link
