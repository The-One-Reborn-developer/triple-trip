import logging

from app.database.queries.post_user import post_user


def post_user_consumer(ch, method, properties, body) -> None:
    logging.info(f" [x] Received {body.decode()}")
    telegram_id = int(body.decode())

    post_user_result = post_user(telegram_id)
    
    if post_user_result:
        logging.info(f'User {telegram_id} added to the database')
    else:
        logging.error(f'Error in post_user_consumer adding user {telegram_id} to the database')

    ch.basic_ack(delivery_tag=method.delivery_tag)