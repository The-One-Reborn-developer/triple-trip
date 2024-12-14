import logging
import orjson

from app.tasks.base import RabbitmqBase


def update_user_producer(telegram_id: int, **kwargs) -> bool:
    try:
        rabbitmq = RabbitmqBase()
        rabbitmq.connect()

        message = {
            'telegram_id': telegram_id,
            **kwargs
        }

        rabbitmq.channel.basic_publish(
            exchange='',
            routing_key='update_user_queue',
            body=orjson.dumps(message)
        )

        logging.info(f'User {telegram_id} with {kwargs} sent through database queue to be updated in the database')
        return True
    except Exception as e:
        logging.error(f'Error in update_user_producer updating user in the database: {e}')
        return False