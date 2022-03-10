import sys

import pika
from loguru import logger

import config


def on_message(ch, method, properties, body):
    """A callback function that do something with the received message."""
    str_body = body.decode('utf-8')
    print(f'[x] Received: {method.routing_key}:{str_body}')


def run():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.BROKER_HOST))
    channel = connection.channel()

    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    severities = sys.argv[1:]
    if not severities:
        str_severities = ' '.join([f'[{severity}]' for severity in config.SEVERITIES])
        logger.error(f' [*] Usage: {sys.argv[0]} {str_severities}')
        sys.exit(1)

    # Creates a different bind to each severity.
    for severity in severities:
        if severity not in config.SEVERITIES:
            logger.error(f" [*] Invalid severity name, available: {','.join(config.SEVERITIES)}")
            sys.exit(1)
        
        channel.queue_bind(
            exchange='direct_logs', queue=queue_name, routing_key=severity)

    channel.basic_consume(
        queue=queue_name, auto_ack=True, on_message_callback=on_message)

    logger.debug(' [*] Waiting for logs. To exit press CTRL+C')
    
    channel.start_consuming()


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        logger.info(' [*] Stopping gracefully...')
        sys.exit(0)
    except Exception as err:
        logger.error(err)
