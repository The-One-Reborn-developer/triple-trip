import logging
import orjson

from app.database.queries.update_location import update_location


def update_location_consumer(ch, method, properties, body) -> None:
    logging.info(f" [x] Received {body.decode()}")
    data = orjson.loads(body)

    try:
        update_location_result = update_location(
            location_id=data['location_id'],
            **{key: value for key, value in data.items() if key != 'location_id'}
        )

        if update_location_result:
            logging.info(f'Location  updated with data {data} in the database')
        else:
            logging.error(f'Error in update_user_consumer updating user {data["telegram_id"]} in the database')
    except Exception as e:
        logging.error(f'Error in update_location_consumer updating location in the database: {e}')
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)