import sys

import pika
from loguru import logger

from ..config import BROKER_HOST


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=BROKER_HOST)
)
channel = connection.channel()
exchange_name = 'task_exchange'
routing_key = 'task_queue'

channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

message = ' '.join(sys.argv[1:]) or 'Hello, World!'
channel.basic_publish(
    exchange=exchange_name,
    routing_key=routing_key,
    body=message,
)

logger.info(f" [x] Sent '{message}'")

connection.close()
