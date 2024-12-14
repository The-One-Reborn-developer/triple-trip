import logging
import orjson

from app.tasks.base import RabbitmqBase


def update_location_producer(location_id: int, **kwargs) -> bool:
    try:
        rabbitmq = RabbitmqBase()
        rabbitmq.connect()

        message = {
            'location_id': location_id,
            **kwargs
        }

        rabbitmq.channel.basic_publish(
            exchange='',
            routing_key='update_location_queue',
            body=orjson.dumps(message)
        )

        logging.info(f'Location {location_id} with {kwargs} sent through database queue to be updated in the database')
        return True
    except Exception as e:
        logging.error(f'Error in update_location_producer updating location in the database: {e}')
        return False