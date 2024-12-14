import logging
import orjson

from app.tasks.base import RabbitmqBase


def post_location_producer(location: dict) -> bool:
    try:
        rabbitmq = RabbitmqBase()
        rabbitmq.connect()

        rabbitmq.channel.basic_publish(
            exchange='',
            routing_key='post_location_queue',
            body=orjson.dumps(location)
        )

        logging.info(f'Location {location.get("name")} sent through database queue to be added to the database')
        return True
    except Exception as e:
        logging.error(f'Error in post_location_producer adding location to the database: {e}')
        return False