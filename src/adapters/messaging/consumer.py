import json
import pika
import pika.adapters.blocking_connection
import pika.credentials
from src.infra.usecase import UseCase


class Consumer:
    def __init__(
        self,
        queue_name: str,
        usecase: UseCase,
        channel: pika.adapters.blocking_connection.BlockingChannel,
    ):
        self.queue_name = queue_name
        self.usecase = usecase
        self.channel = channel

    def consumer_handler(self, channel, method_frame, header_frame, body):
        json_data = json.loads(body.decode('utf-8'))
        
        try:
            self.usecase.execute(json_data)
            self.channel.basic_ack(method_frame.delivery_tag)
        except Exception as e:
            print(f"Error processing message {e}")
            self.channel.basic_nack(method_frame.delivery_tag)

    def prepare(self):
        self.channel.basic_consume(self.queue_name, self.consumer_handler)
        return
