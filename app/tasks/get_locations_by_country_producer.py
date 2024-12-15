import logging
import pika
import uuid
import orjson

from app.tasks.base import RabbitmqBase


def get_locations_by_country_producer(country_code: str) -> list[dict] | bool:
    try:
        rabbitmq = RabbitmqBase()
        rabbitmq.connect()

        correlation_id = str(uuid.uuid4())

        rabbitmq.channel.basic_publish(
            exchange='',
            routing_key='get_locations_by_country_queue',
            body=str(country_code),
            properties=pika.BasicProperties(
                reply_to='get_locations_by_country_reply_queue',
                correlation_id=correlation_id
            )
        )

        logging.info(f'Country {country_code} sent through database queue to get locations from the database')

        response = None
        for method_frame, properties, body in rabbitmq.channel.consume('get_locations_by_country_reply_queue'):
            if properties.correlation_id == correlation_id:
                response = orjson.loads(body)
                logging.info(f'Response from the database: {response}, type: {type(response)}')
                rabbitmq.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                break

        rabbitmq.close()

        if response:
            logging.info(f'Response from the database: {response}, type: {type(response)}')
            return response
        else:
            logging.error('Unexpected response from the database')
            return False
    except Exception as e:
        logging.error(f'Error in get_locations_by_country_producer getting locations from the database: {e}')
        return False