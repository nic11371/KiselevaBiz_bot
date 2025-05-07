import logging
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, \
    setup_application
from create_bot import bot, dp, BASE_URL, WEBHOOK_PATH, HOST, PORT, ADMIN_ID
from utils.db import initialize_database
from handlers.start import router as start_router
from handlers.admin_panel import router as admin_router


async def set_commands():
    commands = [BotCommand(command="start", description="Старт")]
    await bot.set_my_commands(commands, BotCommandScopeDefault)


async def on_startup() -> None:
    await set_commands()
    await initialize_database()
    await bot.set_webhook(f"{BASE_URL}{WEBHOOK_PATH}")
    await bot.send_message(chat_id=ADMIN_ID, text="Бот запущен")


async def on_shutdown() -> None:
    await bot.send_message(chat_id=ADMIN_ID, text="Бот остановлен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()


def main() -> None:
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=HOST, port=PORT)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    main()
