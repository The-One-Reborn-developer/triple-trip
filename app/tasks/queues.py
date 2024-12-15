import time
import logging

from app.tasks.base import RabbitmqBase
from app.tasks.post_user_consumer import post_user_consumer
from app.tasks.create_tables_consumer import create_tables_consumer
from app.tasks.update_user_consumer import update_user_consumer
from app.tasks.post_location_consumer import post_location_consumer
from app.tasks.get_user_consumer import get_user_consumer
from app.tasks.get_unvalidated_locations_consumer import get_unvalidated_locations_consumer
from app.tasks.update_location_consumer import update_location_consumer
from app.tasks.delete_location_consumer import delete_location_consumer
from app.tasks.get_locations_by_country_consumer import get_locations_by_country_consumer


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logging.info('Waiting for RabbitMQ to be ready')
    time.sleep(30)

    rabbitmq = RabbitmqBase()

    rabbitmq.connect()
    rabbitmq.declare_queues()
    rabbitmq.channel.basic_qos(prefetch_count=1)

    rabbitmq.channel.basic_consume(
        queue='post_user_queue',
        on_message_callback=post_user_consumer
    )
    rabbitmq.channel.basic_consume(
        queue='create_tables_queue',
        on_message_callback=create_tables_consumer
    )
    rabbitmq.channel.basic_consume(
        queue='update_user_queue',
        on_message_callback=update_user_consumer
    )
    rabbitmq.channel.basic_consume(
        queue='post_location_queue',
        on_message_callback=post_location_consumer
    )
    rabbitmq.channel.basic_consume(
        queue='get_user_queue',
        on_message_callback=get_user_consumer
    )
    rabbitmq.channel.basic_consume(
        queue='get_unvalidated_locations_queue',
        on_message_callback=get_unvalidated_locations_consumer
    )
    rabbitmq.channel.basic_consume(
        queue='update_location_queue',
        on_message_callback=update_location_consumer
    )
    rabbitmq.channel.basic_consume(
        queue='delete_location_queue',
        on_message_callback=delete_location_consumer
    )
    rabbitmq.channel.basic_consume(
        queue='get_locations_by_country_queue',
        on_message_callback=get_locations_by_country_consumer
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