import logging
import orjson

from app.database.queries.post_location import post_location


def post_location_consumer(ch, method, properties, body) -> None:
    logging.info(f" [x] Received {body.decode()}")
    try:
        location_data = orjson.loads(body)

        required_keys = ['country', 'name', 'address', 'photos']
        if not required_keys.issubset(location_data.keys()):
            raise ValueError('Invalid location data')

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

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f'Error in post_location_consumer adding location to the database: {e}')
        ch.basic_ack(delivery_tag=method.delivery_tag)