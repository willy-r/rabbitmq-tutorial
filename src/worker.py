import sys
import time

import pika
from loguru import logger

import config


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
        pika.ConnectionParameters(host=config.BROKER_HOST)) 
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue='task_queue', on_message_callback=on_message)

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
