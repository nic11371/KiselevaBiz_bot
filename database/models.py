import os
from sqlalchemy import BigInteger, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, \
    create_async_engine
from datetime import datetime

engine = create_async_engine(
    url='sqlite+aiosqlite:///data/db.sqlite3', echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    status_pay: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_pay_date: Mapped[datetime] = mapped_column(
        DateTime, default=None, nullable=True)


async def async_main():
    if not os.path.exists("data/db.sqlite3"):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
