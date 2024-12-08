import os

from sqlalchemy import create_engine

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

sync_engine = create_engine(
    os.getenv('DATABASE_URL'),
    echo=True
)