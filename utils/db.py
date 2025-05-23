import aiosqlite
from create_bot import DATABASE_PATH


async def initialize_database():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Создаем таблицу users, если она не существует
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                bot_open BOOLEAN DEFAULT FALSE,
                block BOOLEAN DEFAULT FALSE
            )
        """)
        # Сохраняем изменения
        await db.commit()


async def add_user(telegram_id: int, username: str, first_name: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO users (telegram_id, username, first_name)
            VALUES (?, ?, ?)
            ON CONFLICT(telegram_id) DO NOTHING
        """, (telegram_id, username, first_name))
        await db.commit()


async def get_all_users():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()

        # Преобразуем результаты в список словарей
        users = [
            {
                "telegram_id": row[0],
                "username": row[1],
                "first_name": row[2],
                "bot_open": bool(row[3]),
                "block": bool(row[4])
            }
            for row in rows
        ]
        return users


async def get_user_by_id(telegram_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        row = await cursor.fetchone()

        if row is None:
            return None

        # Преобразуем результат в словарь
        user = {
            "telegram_id": row[0],
            "username": row[1],
            "first_name": row[2],
            "bot_open": bool(row[3]),
            "block": bool(row[4])
        }
        return user


async def update_bot_open_status(telegram_id: int, bot_open: bool):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            UPDATE users
            SET bot_open = ?
            WHERE telegram_id = ?
        """, (bot_open, telegram_id))
        await db.commit()


async def update_block_status(telegram_id: int, block: bool):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            UPDATE users
            SET block = ?
            WHERE telegram_id = ?
        """, (block, telegram_id))
        await db.commit()
