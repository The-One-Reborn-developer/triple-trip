from app.database.models.async_engine import async_engine
from sqlalchemy.ext.asyncio import AsyncSession


async_session = AsyncSession(async_engine, expire_on_commit=False)