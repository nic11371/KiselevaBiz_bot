import os
# from decouple import config
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from aiogram.fsm.storage.memory import MemoryStorage


load_dotenv()


ADMIN_ID = int(os.getenv('ADMIN_ID'))
BOT_TOKEN = os.getenv("BOT_TOKEN")
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
WEBHOOK_PATH = f'/{BOT_TOKEN}'
BASE_URL = os.getenv("BASE_URL")
DATABASE_PATH = os.getenv("DATABASE_PATH")

# ADMIN_ID = int(config('ADMIN_ID'))
# BOT_TOKEN = config("BOT_TOKEN")
# HOST = config("HOST")
# PORT = int(config("PORT"))
# WEBHOOK_PATH = f'/{BOT_TOKEN}'
# BASE_URL = config("BASE_URL")


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(
    parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
kb_list = [{
    'label': 'ПРОДАЖИ БЕЗ МАСОК',
    'url': 'https://t.me/KiselevaBiz'
}]
