import logging
import pika
import orjson

from app.database.queries.get_unvalidated_locations import get_unvalidated_locations


def get_unvalidated_locations_consumer(ch, method, properties, body) -> None:
    logging.info(f" [x] Received {body.decode()}")

    get_unvalidated_locations_result = get_unvalidated_locations()

    if get_unvalidated_locations_result:
        response = [location_to_dict(location) for location in get_unvalidated_locations_result]
        logging.info(f'Found {len(get_unvalidated_locations_result)} unvalidated locations in the database')

        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            body=orjson.dumps(get_unvalidated_locations_result),
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id
            )
        )
    else:
        logging.info(f'No unvalidated locations found in the database')

    ch.basic_ack(delivery_tag=method.delivery_tag)


def location_to_dict(location: object) -> dict:
    return {
        'id': location.id,
        'country': location.country,
        'name': location.name,
        'address': location.address,
        'photos': location.photos,
        'is_verified': location.is_verified
    }