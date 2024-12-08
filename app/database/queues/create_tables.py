import logging

from app.database.models.base import Base
from app.database.models.users import User
from app.database.models.async_engine import async_engine


async def create_tables() -> bool |None:
    async with async_engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
            return True
        except Exception as e:
            logging.error(f'Error creating tables: {e}')
            return False