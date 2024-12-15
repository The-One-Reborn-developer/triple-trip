import logging
import pika


class RabbitmqBase:
    def __init__(self):
        self.connection = None
        self.channel = None

    
    def connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters('rabbitmq')
            )
            self.channel = self.connection.channel()
        except Exception as e:
            logging.error(f'Error in RabbitmqBase connecting to RabbitMQ: {e}')
    

    def declare_queues(self):
        try:
            if not self.channel:
                raise RuntimeError('RabbitMQ channel is not initialized')
            else:
                self.channel.queue_declare(
                    queue='post_user_queue',
                    durable=True
                )
                self.channel.queue_declare(
                    queue='create_tables_queue',
                    durable=True
                )
                self.channel.queue_declare(
                    queue='update_user_queue',
                    durable=True
                )
                self.channel.queue_declare(
                    queue='post_location_queue',
                    durable=True
                )
                self.channel.queue_declare(
                    queue='get_user_queue',
                    durable=True
                )
                self.channel.queue_declare(
                    queue='get_user_reply_queue',
                    durable=True
                )
                self.channel.queue_declare(
                    queue='get_unvalidated_locations_queue',
                    durable=True
                )
                self.channel.queue_declare(
                    queue='get_unvalidated_locations_reply_queue',
                    durable=True
                )
                self.channel.queue_declare(
                    queue='update_location_queue',
                    durable=True
                )
                self.channel.queue_declare(
                    queue='delete_location_queue',
                    durable=True
                )
                self.channel.queue_declare(
                    queue='get_locations_by_country_queue',
                    durable=True
                )
                self.channel.queue_declare(
                    queue='get_locations_by_country_reply_queue',
                    durable=True
                )
        except Exception as e:
            logging.error(f'Error in RabbitmqBase declaring queues: {e}')


    def close(self):
        if self.connection:
            self.connection.close()