import aiosqlite, logging, os
from typing import Union

class Database:
    def __init__(self):
        self.database = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "database", "mailgram.db"))
        
    async def create_tables(self):
        async with aiosqlite.connect(self.database) as db:
            async with db.cursor() as cursor:
                await cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER UNIQUE NOT NULL,
                        username TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        language TEXT NOT NULL DEFAULT 'en',
                        credentials TEXT NOT NULL DEFAULT 'NONE'
                    )                 
                    """)
                
                
                logging.info("Tables created successfully.")
                await db.commit()
                
    async def insert_user(self, user_id: int, username: str) -> Union[bool, int, None]:
        try:
            async with aiosqlite.connect(self.database) as db:
                async with db.cursor() as cursor:
                    await cursor.execute(
                        "INSERT INTO users (user_id, username) VALUES (?, ?)",
                        (user_id, username)
                    )
                await db.commit()
                logging.info(f"User {username} with id {user_id} inserted successfully.")
                return True
        except aiosqlite.IntegrityError:
            logging.info(f"User with ID {user_id} already exists.")
            return 409
        except Exception as e:
            logging.error(f"Error inserting user: {e}")
            return None
        
    async def fetch_info(self, user_id: int) -> Union[dict, None]:
        try:
            async with aiosqlite.connect(self.database) as db:
                async with db.cursor() as cursor:
                    await cursor.execute(
                        "SELECT * FROM users WHERE user_id =?",
                        (user_id,)
                    )
                    row = await cursor.fetchone()
                
                if row:
                    return {
                        "id": row[0],
                        "user_id": row[1],
                        "username": row[2],
                        "created_at": row[3],
                        "language": row[4],
                        "credentials": row[5]
                    }
                else:
                    return None
        except Exception as e:
            logging.error(f"Error fetching user info: {e}")
            return None
        
    async def change_info(self, user_id: int, identity: any, value: any) -> Union[bool, None]:
        try:
            async with aiosqlite.connect(self.database) as db:
                async with db.cursor() as cursor:
                    await cursor.execute(
                        f"UPDATE users SET {identity} =? WHERE user_id =?",
                        (value, user_id)
                    )
                    await db.commit()
                    logging.info(f"User info updated successfully.")
                    return True
        except Exception as e:
            logging.error(f"Error updating user info: {e}")
            return None
        