import os

from sqlalchemy.ext.asyncio import create_async_engine

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

async_engine = create_async_engine(
    os.getenv('DATABASE_URL'),
    echo=True,
    future=True
)