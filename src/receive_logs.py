import sys

import pika
from loguru import logger

import config


def on_message(ch, method, properties, body):
    """A callback function that do something with the received message."""
    str_body = body.decode('utf-8')
    print(f'[x] Received: {str_body}')


def run():    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.BROKER_HOST)) 
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Binds the exchange to the queue.
    channel.queue_bind(exchange='logs', queue=queue_name)

    channel.basic_consume(
        queue=queue_name, auto_ack=True, on_message_callback=on_message)

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
