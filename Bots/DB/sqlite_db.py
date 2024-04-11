import aiosqlite

class Db:
    def __init__(self, db_file='database.db'):
        self.db_file = db_file

    async def create_users_table(self):
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT,
                    user_telegram_id VARCHAR(255) NOT NULL UNIQUE,
                    access_token TEXT,
                    refresh_token TEXT
                )
            """)
            await db.commit()

    async def insert_users(self, user_telegram_id, user_name, access_token, refresh_token):
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute("""
                INSERT INTO users (user_telegram_id,user_name, access_token, refresh_token) VALUES (?,?, ?, ?)
                ON CONFLICT(user_telegram_id) DO UPDATE SET access_token = excluded.access_token,user_name=excluded.user_name, refresh_token = excluded.refresh_token
            """, (user_telegram_id,user_name, access_token, refresh_token))
            await db.commit()

    async def update_access_token(self, user_telegram_id, refresh_token, new_access_token):
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute("""
                UPDATE users SET access_token = ?, refresh_token = ? WHERE user_telegram_id = ?
            """, (new_access_token, refresh_token, user_telegram_id))
            await db.commit()

    async def get_refresh_token(self, user_telegram_id):
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute("""
                SELECT refresh_token FROM users WHERE user_telegram_id = ?
            """, (user_telegram_id,)) as cursor:
                result = await cursor.fetchone()
                return result[0] if result else None

    async def get_access_token(self, user_telegram_id):
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute("""
                SELECT access_token FROM users WHERE user_telegram_id = ?
            """, (user_telegram_id,)) as cursor:
                result = await cursor.fetchone()
                return result[0] if result else None

    async def get_all_user_ids_and_refresh_tokens(self)->(str,str):
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute("SELECT user_telegram_id, refresh_token FROM users") as cursor:
                result = await cursor.fetchall()
                return result
