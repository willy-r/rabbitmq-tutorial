import sys

import pika
from loguru import logger

import config


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.BROKER_HOST))
channel = connection.channel()

channel.queue_declare(exchange='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or 'Hello, World!'
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
)

logger.info(f" [x] Sent '{message}'")

connection.close()
