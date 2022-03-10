import sys

import pika
from loguru import logger

import config


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.BROKER_HOST))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'

if severity not in config.SEVERITIES:
    logger.error(f" [*] Invalid severity name, available: {','.join(config.SEVERITIES)}")
    sys.exit(1)

message = ' '.join(sys.argv[2:]) or 'Hello, World!'
channel.basic_publish(
    exchange='direct_logs', routing_key=severity, body=message)

logger.info(f' [x] Sent {severity=}:{message=}')

connection.close()
