import logging

from app.tasks.base import RabbitmqBase


def post_user_producer(telegram_id: int) -> bool:
    try:
        rabbitmq = RabbitmqBase()
        rabbitmq.connect()

        rabbitmq.channel.basic_publish(
            exchange='',
            routing_key='post_user_queue',
            body=str(telegram_id)
        )

        logging.info(f'User {telegram_id} sent through database queue to be added to the database')
        return True
    except Exception as e:
        logging.error(f'Error in post_user_producer adding user to the database: {e}')
        return False