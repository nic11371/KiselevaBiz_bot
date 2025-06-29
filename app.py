import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from handlers.user import user
from handlers.admin import admin
import logging
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from middlewares import AntiSpamMiddleware
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.webhooks import ckassa_webhook
from functools import partial
from database.models import async_main
from handlers.subscription_checker import subscription_checker
# from database.requests import simulate_expired_user

load_dotenv()


# переменные для работы
ADMIN_ID = os.getenv('ADMIN_ID')
BOT_TOKEN = os.getenv("BOT_TOKEN")
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
WEBHOOK_PATH = f'/{BOT_TOKEN}'
BASE_URL = os.getenv("BASE_URL")

# инициализируем бота и диспетчера для работы с ним
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
# dp.update.middleware(AntiSpamMiddleware(limit=2, interval=1))


# async def set_commands():
#     # Создаем список команд, которые будут доступны пользователям
#     commands = [BotCommand(command='start', description='Старт')]
#     # Устанавливаем эти команды как дефолтные для всех пользователей
#     await bot.set_my_commands(commands, BotCommandScopeDefault())


# Функция, которая будет вызвана при запуске бота
async def on_startup() -> None:
    await async_main()
    # Устанавливаем командное меню
    # await set_commands()
    # Устанавливаем вебхук для приема сообщений через заданный URL
    await bot.set_webhook(f"{BASE_URL}{WEBHOOK_PATH}")

    # await simulate_expired_user(tg_id=1000092717, days_ago=30)

    # Отправляем сообщение администратору о том, что бот был запущен
    asyncio.create_task(subscription_checker(bot))
    await bot.send_message(chat_id=ADMIN_ID, text='Бот запущен!')
    webhook_info = await bot.get_webhook_info()
    print("📡 Webhook info:", webhook_info)


# Функция, которая будет вызвана при остановке бота
async def on_shutdown() -> None:
    # Отправляем сообщение администратору о том, что бот был остановлен
    await bot.send_message(chat_id=ADMIN_ID, text='Бот остановлен!')
    # Удаляем вебхук и, при необходимости, очищаем ожидающие обновления
    await bot.delete_webhook(drop_pending_updates=True)
    # Закрываем сессию бота, освобождая ресурсы
    await bot.session.close()


# Основная функция, которая запускает приложение
def main() -> None:
    # Подключаем маршрутизатор (роутер) для обработки сообщений
    dp.include_routers(user, admin)

    # Регистрируем функцию, которая будет вызвана при старте бота
    dp.startup.register(on_startup)

    # Регистрируем функцию, которая будет вызвана при остановке бота
    dp.shutdown.register(on_shutdown)

    # Создаем веб-приложение на базе aiohttp
    app = web.Application()

    # Настраиваем обработчик запросов для работы с вебхуком
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,  # Передаем диспетчер
        bot=bot  # Передаем объект бота
    )
    # Регистрируем обработчик запросов на определенном пути
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    app.router.add_post(
        '/webhook/ckassa', partial(ckassa_webhook, bot=bot, storage=storage))
    # Настраиваем приложение и связываем его с диспетчером и ботом
    setup_application(app, dp, bot=bot)

    # Запускаем веб-сервер на указанном хосте и порте
    web.run_app(app, host=HOST, port=PORT)


# Точка входа в программу
if __name__ == "__main__":
    # Настраиваем логирование (информация, предупреждения, ошибки) и выводим их в консоль
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)  # Создаем логгер для использования в других частях программы
    main()  # Запускаем основную функцию
