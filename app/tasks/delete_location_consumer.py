import logging

from app.database.queries.delete_location import delete_location


def delete_location_consumer(ch, method, properties, body) -> None:
    logging.info(f" [x] Received {body.decode()}")
    location_id = int(body.decode())
    try:
        delete_location_result = delete_location(location_id)

        if delete_location_result:
            logging.info(f'Location {location_id} deleted from the database')
        else:
            logging.error('Error in delete_location_consumer deleting location from the database')
    except:
        logging.error('Error in delete_location_consumer deleting location from the database')
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)