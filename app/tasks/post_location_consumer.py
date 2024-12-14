import logging
import orjson

from app.database.queries.post_location import post_location


def post_location_consumer(ch, method, properties, body) -> None:
    logging.info(f" [x] Received {body.decode()}")
    try:
        location_data = orjson.loads(body)

        required_keys = ['country', 'name', 'address', 'photos']

        for key in required_keys:
            if key not in location_data:
                raise ValueError(f'{key} is a required field')

        location_country = location_data['country']
        location_name = location_data['name']
        location_address = location_data['address']
        location_photos = location_data['photos']

        if not isinstance(location_photos, list):
            raise ValueError('"photos" must be a list')

        post_location_result = post_location(
            country=location_country,
            name=location_name,
            address=location_address,
            photos=location_photos
        )
        
        if post_location_result:
            logging.info(f'Location {location_name} added to the database')
        else:
            logging.error(f'Error in post_location_consumer adding location {location_name} to the database')
    except Exception as e:
        logging.error(f'Error in post_location_consumer adding location to the database: {e}')
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)