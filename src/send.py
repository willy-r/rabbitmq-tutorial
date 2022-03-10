import pika
from loguru import logger

import config


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.BROKER_HOST))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello, World!')

logger.info(" [x] Sent 'Hello, World!'")

connection.close()
