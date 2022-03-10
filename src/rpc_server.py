import sys

import pika
from loguru import logger

import config


def fib(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def on_request(ch, method, props, body):
    n = int(body)
    
    logger.debug(f' [.] fib({n})')
    
    response = fib(n)

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        body=str(response),
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def run():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.BROKER_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='rpc_queue')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

    logger.info(f' [x] Awaiting RPC requests...')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        logger.info(' [*] Stopping gracefully...')
        sys.exit(0)
    except Exception as err:
        logger.error(err)
