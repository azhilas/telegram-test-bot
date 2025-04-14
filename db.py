import aiosqlite

async def init_db():
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_active TIMESTAMP
            )
        """)
        await db.commit()

async def add_user(user):
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (id, username, first_name, last_active)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (user.id, user.username, user.first_name))
        await db.commit()
