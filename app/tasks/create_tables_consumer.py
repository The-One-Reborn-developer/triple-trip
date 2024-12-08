import logging

from app.database.queues.create_tables import create_tables


def create_tables_consumer(ch, method, properties, body) -> None:
    logging.info(f" [x] Received {body.decode()}")
    create_tables_result = create_tables()

    if create_tables_result:
        logging.info('Database tables created')
    else:
        logging.error('Error in create_tables_consumer creating tables')

    ch.basic_ack(delivery_tag=method.delivery_tag)