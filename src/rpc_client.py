import sys
import uuid

import pika
from loguru import logger

import config


class FibonacciRPCClient:

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.BROKER_HOST))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue, auto_ack=True, on_message_callback=self.on_response)
    
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n: int) -> int:
        # Initialize as None, we need to confirm if the request is valid.
        self.response = None
        # Creates a unique correlation id for each call.
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            body=str(n),
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id)
        )

        # Consuming loop.
        while self.response is None:
            self.connection.process_data_events()

        return int(self.response)


fibonacci_rpc = FibonacciRPCClient()
number = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isnumeric() else 0

logger.debug(f' [x] Requesting fib({number})...')
response = fibonacci_rpc.call(number)
logger.debug(f' [.] Got {response}')
