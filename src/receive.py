import sys

import pika
from loguru import logger

import config


def on_message(ch, method, properties, body):
    """A callback function that do something with the received message."""
    str_body = body.decode('utf-8')
    logger.info(f' [x] Received: {str_body}')


def run():    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.BROKER_HOST)) 
    channel = connection.channel()

    channel.basic_consume(
        queue='hello', auto_ack=True, on_message_callback=on_message)

    logger.debug(' [*] Waiting for messages. To exit press CTRL+C')
    
    channel.start_consuming()


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        logger.info(' [*] Stopping gracefully...')
        sys.exit(0)
    except Exception as err:
        logger.error(err)
