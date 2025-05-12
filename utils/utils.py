from aiogram.enums import ChatMemberStatus
from create_bot import bot


async def is_user_subscribed(channel_url: str, telegram_id: int) -> bool:
    try:
        # Получаем username канала из URL
        channel_username = channel_url.split('/')[-1]

        # Получаем информацию о пользователе в канале
        member = await bot.get_chat_member(
            chat_id=f"@{channel_username}", user_id=telegram_id)

        # Проверяем статус пользователя
        if member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.CREATOR,
            ChatMemberStatus.ADMINISTRATOR
        ]:
            return True
        else:
            return False
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")
        return False
