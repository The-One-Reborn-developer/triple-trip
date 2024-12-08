import asyncio
import logging

from app.tasks.base import RabbitmqBase
from app.tasks.post_user_consumer import post_user_consumer


async def main():
    rabbitmq = RabbitmqBase()

    await rabbitmq.connect()

    await rabbitmq.channel.basic_qos(prefetch_count=1)

    await rabbitmq.channel.basic_consume(
        queue='post_user_queue',
        on_message_callback=post_user_consumer
    )

    logging.info(' [*] Waiting for messages.')
    try:
        await rabbitmq.channel.start_consuming()
    except KeyboardInterrupt:
        await rabbitmq.channel.stop_consuming()
        await rabbitmq.connection.close()
        logging.info('RabbitMQ connection closed')


if __name__ == '__main__':
    asyncio.run(main())