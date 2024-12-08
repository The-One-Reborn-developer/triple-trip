import asyncio
import logging

from app.tasks.base import RabbitmqBase
from app.tasks.post_user_consumer import post_user_consumer
from app.tasks.create_tables_consumer import create_tables_consumer


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    rabbitmq = RabbitmqBase()

    rabbitmq.connect()
    rabbitmq.channel.basic_qos(prefetch_count=1)
    rabbitmq.declare_queues()

    rabbitmq.channel.basic_consume(
        queue='post_user_queue',
        on_message_callback=post_user_consumer
    )

    rabbitmq.channel.basic_consume(
        queue='create_tables_queue',
        on_message_callback=create_tables_consumer
    )

    logging.info(' [*] Waiting for messages.')
    try:
        rabbitmq.channel.start_consuming()
    except KeyboardInterrupt or SystemExit:
        rabbitmq.channel.stop_consuming()
        rabbitmq.connection.close()
        logging.info('RabbitMQ connection closed')


if __name__ == '__main__':
    main()