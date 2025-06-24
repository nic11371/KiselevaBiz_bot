from sqlalchemy import select
from database.models import User, async_session


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
        return user


async def save_info_user(tg_id, username, first_name='', last_name=''):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
        await session.commit()
