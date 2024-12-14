import logging
import pika

from app.database.queries.get_user_admin import get_user_admin


def get_user_consumer(ch, method, properties, body) -> None:
    logging.info(f" [x] Received {body.decode()}")
    telegram_id = int(body.decode())

    try:
        get_user_result = get_user_admin(telegram_id)

        if get_user_result:
            response = True
            logging.info(f'Admin {telegram_id} found in the database')

            ch.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                body=str(response),
                properties=pika.BasicProperties(
                    correlation_id=properties.correlation_id
                )
            )
        else:
            logging.info(f'Admin {telegram_id} not found in the database')
    except:
        logging.error(f'Error in get_user_consumer getting user from the database')
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)