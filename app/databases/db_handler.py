import aiosqlite
import asyncio
from aiogram.fsm.state import State
from abc import ABC, abstractmethod

class DatabaseConnection(ABC):
    def __init__(self, db_path):
        self.db_path = db_path
        self.lock = asyncio.Lock()
        self.db = None

    async def __aenter__(self):
        self.db = await aiosqlite.connect(self.db_path)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.db.close()

    @abstractmethod
    async def add_elem(self, *args):
        pass

    @abstractmethod
    async def fetch_elem(self, *args):
        pass


class UserDatabase(DatabaseConnection):
    def __init__(self,db_path):
        super().__init__(db_path)
    
    async def add_elem(self, user_id: int, name: str, tag: str, rights):
        async with self.lock:
            try:
                await self.db.execute('''
                    INSERT INTO users (user_id, name, tag, rights) VALUES (?,?,?,?)
                    ''', (user_id, name, tag, rights))
                await self.db.commit()
                return 1
            except aiosqlite.IntegrityError:
                return 0

    async def fetch_elem(self, user_id: int):
        async with self.lock:
            async with self.db.execute(f'''
                SELECT name, tag
                FROM users
                WHERE user_id = ?
                ''', (user_id,)) as cursor:
                user_data = await cursor.fetchone()
                return bool(user_data)
    
    async def chmod(self, user_id: int):
        async with self.lock:
            await self.db.execute('UPDATE users SET rights = 2 WHERE user_id = ?', (user_id,))
            await self.db.commit()


class RoomsDatabase(DatabaseConnection):
    def __init__(self,db_path):
        super().__init__(db_path)
    
    async def add_elem(self, user_id: int, tag: str, room: str, datetime: str):
        async with self.lock:
            try:
                await self.db.execute('''
                    INSERT INTO users (user_id, tag, room, datetime) VALUES (?,?,?,?)
                    ''', (user_id, tag, room, datetime))
                await self.db.commit()
                return 1
            except aiosqlite.IntegrityError:
                return 0