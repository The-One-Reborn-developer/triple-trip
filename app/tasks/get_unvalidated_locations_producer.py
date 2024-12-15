import logging
import pika
import uuid
import orjson

from app.tasks.base import RabbitmqBase


def get_unvalidated_locations_producer() -> list[dict] | bool:
    try:
        rabbitmq = RabbitmqBase()
        rabbitmq.connect()

        correlation_id = str(uuid.uuid4())

        rabbitmq.channel.basic_publish(
            exchange='',
            routing_key='get_unvalidated_locations_queue',
            body='',
            properties=pika.BasicProperties(
                reply_to='get_unvalidated_locations_reply_queue',
                correlation_id=correlation_id
            )
        )

        logging.info('Request to get unvalidated locations sent through database queue')

        response = None
        for method_frame, properties, body in rabbitmq.channel.consume('get_unvalidated_locations_reply_queue'):
            if properties.correlation_id == correlation_id:
                response = orjson.loads(body)
                logging.info(f'Response from the database: {response}, type: {type(response)}')
                rabbitmq.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                break

        rabbitmq.close()

        if response:
            logging.info(f'Found {len(response)} unvalidated locations in the database')
            return response
        else:
            logging.error(f'Unexpected response from the database: {response}')
            return False
    except Exception as e:
        logging.error(f'Error in get_user_producer fetching user from the database: {e}')
        return False