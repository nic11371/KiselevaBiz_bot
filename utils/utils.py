from aiogram.enums import ContentType, ChatMemberStatus
from create_bot import bot


async def is_user_subscribed(channel_url: str, telegram_id: int) -> bool:
    try:
        channel_username = channel_url.split('/')[-1]
        member = await bot.get_chat_member(
            chat_id=f"@{channel_username}",
            user_id=telegram_id
        )
        if member.status in [
                ChatMemberStatus.MEMBER,
                ChatMemberStatus.CREATOR,
                ChatMemberStatus.ADMINISTRATOR]:
            return True
        else:
            return False
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")
        return False
