import logging

from app.database.models.locations import Location
from app.database.models.sync_session import sync_session


def post_location(
        country: str,
        name: str,
        address: str,
        photos: list[str]
    ) -> bool:
    try:
        if len(photos) > 10:
            raise ValueError(f'Too many photos ({len(photos)}), maximum is 10')
        
        with sync_session() as session:
            with session.begin():
                location = Location(
                    country=country,
                    name=name,
                    address=address,
                    photos=photos
                )
                session.add(location)

                return True
    except Exception as e:
        logging.error(f'Error in post_location adding location {name} to the database: {e}')
        return False