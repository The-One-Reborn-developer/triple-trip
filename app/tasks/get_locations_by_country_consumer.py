import logging
import pika
import orjson

from app.database.queries.get_locations_by_country import get_locations_by_country


def get_locations_by_country_consumer(ch, method, properties, body) -> None:
    logging.info(f" [x] Received {body.decode()}")

    try:
        get_locations_by_country_result = get_locations_by_country(body.decode())


        if get_locations_by_country_result:
            logging.info(f'Found {len(get_locations_by_country_result)} locations in the database')

            ch.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                body=orjson.dumps(get_locations_by_country_result),
                properties=pika.BasicProperties(
                    correlation_id=properties.correlation_id
                )
            )
        else:
            logging.info(f'No locations found in the database')

            ch.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                body=orjson.dumps([]),
                properties=pika.BasicProperties(
                    correlation_id=properties.correlation_id
                )
            )
    except Exception as e:
        logging.error(f'Error in get_locations_by_country_consumer getting locations from the database: {e}')
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)