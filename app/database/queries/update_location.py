import logging

from sqlalchemy import select

from app.database.models.locations import Location
from app.database.models.sync_session import sync_session

def update_location(location_id: int, **kwargs) -> bool:
    try:
        with sync_session() as session:
            with session.begin():
                user = session.scalar(select(Location).
                                      where(Location.id == location_id))

                if user:
                    for key, value in kwargs.items():
                        setattr(user, key, value)

                    logging.info(f'Location {location_id} updated with data {kwargs} in the database')

                    session.add(user)

                    return True
                else:
                    logging.info(f'Location {location_id} does not exist in the database')
                    return False
    except Exception as e:
        logging.error(f'Error in update_user updating user in database: {e}')
        return False