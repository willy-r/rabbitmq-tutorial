import sys

import pika
from loguru import logger

import config


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.BROKER_HOST))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

# <facility>.<severity>
routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'

if routing_key.count('.') != 1:
    logger.error(' [x] Routing key must be in the format <facility>.<severity>')
    sys.exit(1)

message = ' '.join(sys.argv[2:]) or 'Hello, World!'
channel.basic_publish(
    exchange='topic_logs', routing_key=routing_key, body=message)

logger.info(f' [x] Sent {routing_key=}:{message=}')

connection.close()
