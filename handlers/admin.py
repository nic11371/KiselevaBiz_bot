import os
from aiogram import Router
from aiogram.filters import Filter, Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

admin = Router()

ADMIN_ID = int(os.getenv("ADMIN", "0"))


class Admin(Filter):
    def __init__(self):
        self.admin_id = ADMIN_ID

    async def __call__(self, message: Message):
        return message.from_user.id == self.admin_id


@admin.message()
async def get_group_id(message: Message):
    await message.answer(f"Chat ID: `{message.chat.id}`", parse_mode="Markdown")
