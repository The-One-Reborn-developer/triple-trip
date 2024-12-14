import logging
import orjson

from app.database.queries.update_user import update_user


def update_user_consumer(ch, method, properties, body) -> None:
    logging.info(f" [x] Received {body.decode()}")
    data = orjson.loads(body)

    try:
        update_user_result = update_user(
            telegram_id=data['telegram_id'],
            **{key: value for key, value in data.items() if key != 'telegram_id'}
        )

        if update_user_result:
            logging.info(f'User {data["telegram_id"]} updated with data {data} in the database')
        else:
            logging.error(f'Error in update_user_consumer updating user {data["telegram_id"]} in the database')
    except:
        logging.error(f'Error in update_user_consumer updating user in the database')
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)