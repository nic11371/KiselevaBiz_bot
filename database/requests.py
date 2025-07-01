from sqlalchemy import select
from datetime import datetime, timedelta
from database.models import User, async_session


async def get_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        print(f"[DEBUG] get_user: {user.tg_id}-> status_pay={user.status_pay}")
        return user


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
        return user


async def save_info_user(
        tg_id, username=None, first_name=None, last_name=None):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
        await session.commit()


async def update_status(tg_id, status):
    async with async_session() as session:
        u = await session.scalar(select(User).where(User.tg_id == tg_id))
        if u:
            u.status_pay = status
            u.date = datetime.utcnow()
            u.last_pay_date = datetime.utcnow() + timedelta(days=30)
            await session.commit()


async def get_all_users():
    async with async_session() as session:
        return (await session.scalars(select(User))).all()
