import logging
import pika
import uuid

from app.tasks.base import RabbitmqBase


def get_user_producer(telegram_id: int) -> bool:
    try:
        rabbitmq = RabbitmqBase()

        rabbitmq.connect()

        correlation_id = str(uuid.uuid4())

        rabbitmq.channel.basic_publish(
            exchange='',
            routing_key='get_user_queue',
            body=str(telegram_id),
            properties=pika.BasicProperties(
                reply_to='get_user_reply_queue',
                correlation_id=correlation_id
            )
        )

        logging.info(f'User {telegram_id} sent through database queue to be fetched from the database')

        response = None
        for method_frame, properties, body in rabbitmq.channel.consume('get_user_reply_queue'):
            if properties.correlation_id == correlation_id:
                response = body.decode()
                rabbitmq.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                break

        rabbitmq.close()

        if response == 'True':
            return True
        elif response == 'False':
            return False
        else:
            logging.error(f'Unexpected response from the database: {response}')
            return False
    except Exception as e:
        logging.error(f'Error in get_user_producer fetching user from the database: {e}')
        return False