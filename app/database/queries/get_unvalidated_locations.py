import logging

from sqlalchemy import select

from app.database.models.locations import Location
from app.database.models.sync_session import sync_session


def get_unvalidated_locations() -> list[Location]:
    try:
        with sync_session() as session:
            with session.begin():
                locations = session.scalars(select(Location)
                                            .where(Location.is_verified == False)).all()

                if locations:
                    logging.info(f'Found {len(locations)} unvalidated locations in the database')
                    
                    return [
                        {
                            'id': location.id,
                            'country': location.country,
                            'name': location.name,
                            'address': location.address,
                            'photos': location.photos,
                            'is_verified': location.is_verified
                        } for location in locations
                    ]
                else:
                    logging.info(f'No unvalidated locations found in the database')
                    return []
    except Exception as e:
        logging.error(f'Error in get_unvalidated_locations getting unvalidated locations from database: {e}')
        return []