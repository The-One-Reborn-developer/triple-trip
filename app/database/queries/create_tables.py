import logging

from app.database.models.base import Base
from app.database.models.users import User
from app.database.models.locations import Location
from app.database.models.sync_engine import sync_engine


def create_tables() -> bool |None:
    try:
        with sync_engine.begin() as connection:
            Base.metadata.create_all(connection)
            return True
    except Exception as e:
        logging.error(f'Error in create_tables creating tables: {e}')
        return False