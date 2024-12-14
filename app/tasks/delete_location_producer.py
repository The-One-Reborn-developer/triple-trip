import logging

from app.tasks.base import RabbitmqBase


def delete_location_producer(location_id: int) -> bool:
    try:
        rabbitmq = RabbitmqBase()
        rabbitmq.connect()

        rabbitmq.channel.basic_publish(
            exchange='',
            routing_key='delete_location_queue',
            body=str(location_id)
        )

        logging.info(f'Location {location_id} sent through database queue to be deleted in the database')
        return True
    except Exception as e:
        logging.error(f'Error in update_location_producer deleting location in the database: {e}')
        return False