from sqlalchemy import select
from datetime import datetime, timedelta
from database.models import User, async_session


async def get_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        print(f"[DEBUG] get_user: {user.tg_id} -> status_pay={user.status_pay}")
        return user


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


async def update_status(tg_id, status):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.status_pay = status
            user.date = datetime.utcnow()
            await session.commit()


async def get_all_users():
    async with async_session() as session:
        return (await session.scalars(select(User))).all()


async def update_user_status(tg_id, status: bool):
    async with async_session() as session:
        u = await session.scalar(select(User).where(User.tg_id == tg_id))
        if u:
            u.status_pay = status
            u.date = datetime.utcnow()
            await session.commit()


async def update_last_reminder_date(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.last_reminder_date = datetime.utcnow()
            await session.commit()


async def simulate_expired_user(tg_id, days_ago: int = 30):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.last_pay_date = datetime.utcnow() - timedelta(days=days_ago)
            # user.status_pay = False
            await session.commit()
