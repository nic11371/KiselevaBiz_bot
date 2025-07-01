from sqlalchemy import select
from datetime import datetime, timedelta
from variables import PREV_LAST_DATE, LAST_DATE
from database.models import User, async_session


async def simulate_prev_expired_user(tg_id, days_ago=PREV_LAST_DATE):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.last_pay_date = datetime.utcnow() - timedelta(days=days_ago)
            user.status_pay = True
            await session.commit()


async def simulate_expired_user(tg_id, days_ago=LAST_DATE):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.last_pay_date = datetime.utcnow() - timedelta(days=days_ago)
            user.status_pay = True
            await session.commit()
