from aiogram.types import BotCommand


commands = [
    BotCommand(command="/start", description="Запуск бота"),
    BotCommand(command="/admin", description="Админ панель"),
    BotCommand(command="/place", description="Местоположение"),
    BotCommand(command="/test", description="Тестирование бота"),
    BotCommand(command="/donate", description="Задонатить проект"),
    BotCommand(command="/subscription", description="Оплатить подписку"),
    BotCommand(command="/order", description="Заказать доставку"),
]
