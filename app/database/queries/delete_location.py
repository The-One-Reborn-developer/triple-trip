import logging

from sqlalchemy import delete

from app.database.models.locations import Location
from app.database.models.sync_session import sync_session


async def delete_location(location_id: int) -> bool:
    try:
        await sync_session.execute(
            delete(Location).where(Location.location_id == location_id)
        )
        return True
    except Exception as e:
        logging.error(f'Error in delete_location deleting location in the database: {e}')
        return False