import logging

from app.tasks.base import RabbitmqBase


def create_tables_producer() -> bool:
    try:
        rabbitmq = RabbitmqBase()
        rabbitmq.connect()

        rabbitmq.channel.basic_publish(
            exchange='',
            routing_key='create_tables_queue',
            body='create_tables'
        )

        logging.info('Request to create tables sent through database queue')
        return True
    except Exception as e:
        logging.error(f'Error in create_tables_producer creating tables: {e}')
        return False