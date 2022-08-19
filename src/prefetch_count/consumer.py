import sys
import time

import pika
from loguru import logger

from ..config import BROKER_HOST


def on_message(ch, method, properties, body):
    """A callback function that do something with the received message."""
    str_body = body.decode('utf-8')
    task_seconds = str_body.count('.')
    
    logger.info(f' [x] Received: {str_body}')
    time.sleep(task_seconds)  # Simulates a time-consuming task.
    logger.info(' [x] Done!')
    # Sends a proper ack(nowledgment) from the worker.
    ch.basic_ack(delivery_tag=method.delivery_tag)


def run():    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=BROKER_HOST)
    ) 
    channel = connection.channel()
    exchange_name = 'task_exchange'
    routing_key = 'task_queue'
    
    channel.exchange_declare(exchange=exchange_name, exchange_type="direct")
    result = channel.queue_declare(queue=routing_key)

    channel.queue_bind(
        exchange=exchange_name,
        queue=result.method.queue,
        routing_key=routing_key,
    )
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=result.method.queue, on_message_callback=on_message
    )

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
