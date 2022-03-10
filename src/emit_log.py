import sys

import pika
from loguru import logger

import config


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.BROKER_HOST))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or 'Hello, World!'
channel.basic_publish(
    exchange='logs', routing_key='', body=message)

logger.info(f" [x] Sent '{message}'")

connection.close()
