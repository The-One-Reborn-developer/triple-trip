import logging

from sqlalchemy import delete

from app.database.models.locations import Location
from app.database.models.sync_session import sync_session


def delete_location(location_id: int) -> bool:
    try:
        with sync_session() as session:
            with session.begin():
                session.execute(delete(Location).where(Location.id == location_id))

                logging.info(f'Location {location_id} deleted from the database')
        return True
    except Exception as e:
        logging.error(f'Error in delete_location deleting location in the database: {e}')
        return False