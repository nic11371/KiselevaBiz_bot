import time
from collections import defaultdict
from datetime import time
from typing import Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


user_messages = defaultdict(list)


class AntiSpamMiddleware(BaseMiddleware):
    def __init__(self, limit: int, interval: float):
        super().__init__()
        self.limit = limit
        self.interval = interval

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, any]], Awaitable[any]],
        event: TelegramObject,
        data: Dict[str, any]
    ) -> any:

        message: Message = data.get('message')
        if not message:
            return await handler(event, data)

        user_id = message.from_user.id
        current_time = time()
        user_messages[user_id] = [
            msg_time for msg_time in user_messages[user_id]
            if current_time - msg_time <= self.interval
        ]
        user_messages[user_id].append(current_time)
        if len(user_messages[user_id]) > self.limit:
            await event.message.delete()
            await self.bot.send_message(
                user_id, 'Слишком много сообщений. Попробуйте позже.')
            return
        return await handler(event, data)
