import asyncio

import pika.adapters.asyncio_connection


class RabbitmqBase:
    def __init__(self):
        self.connection = None
        self.channel = None

    async def connect(self):
        loop = asyncio.get_event_loop()

        self.connection = pika.adapters.asyncio_connection.AsyncioConnection(
            pika.ConnectionParameters(
                host='localhost',
                port=5672
            ),
            loop=loop
        )

        self.channel = await self.connection.channel()

        await self.channel.queue_declare(
            queue='create_tables_queue',    
            durable=True
        )

        await self.channel.queue_declare(
            queue='post_user_queue',
            durable=True
        )