import os
from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv('ADMIN_ID')
PAYMENTS_PAYMASTER = os.getenv("PAYMENTS_PAYMASTER")
DOMAIN_PAY = os.getenv("DOMAIN_PAY")
COST = os.getenv("COST")
CURRENCY = os.getenv("CURRENCY")
SECRET = os.getenv("SECRET")
TIME = os.getenv("TIME")
CHAT_ID = os.getenv("CHAT_ID")
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
BASE_URL = os.getenv("BASE_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
LAST_DATE = os.getenv("LAST_DATE")
PREV_LAST_DATE = os.getenv("PREV_LAST_DATE")
WEBHOOK_PATH = f'/{BOT_TOKEN}'
