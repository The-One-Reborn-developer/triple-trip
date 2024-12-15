import logging

from sqlalchemy import select

from app.database.models.locations import Location
from app.database.models.sync_session import sync_session


def get_locations_by_country(country: str) -> list[Location]:
    try:
        with sync_session() as session:
            with session.begin():
                locations = session.scalars(select(Location)
                                            .where(Location.country == country, Location.is_verified == True)).all()

                if locations:
                    logging.info(f'Found {len(locations)} locations in the database for country {country}')
                    
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
                    logging.info(f'No locations found in the database for country {country}')
                    return []
    except Exception as e:
        logging.error(f'Error in get_locations_by_country getting locations from database: {e}')
        return []