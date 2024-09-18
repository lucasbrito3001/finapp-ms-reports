import json
import pika
import pika.adapters.blocking_connection
import pika.credentials


class RabbitMQPublisher:
    def __init__(
        self,
        channel: pika.adapters.blocking_connection.BlockingChannel,
    ):
        self.channel = channel

    def publish(self, exchange_name: str, routing_key: str, message_payload: dict):
        payload_stringified = json.dumps(message_payload)

        self.channel.basic_publish(exchange_name, routing_key, payload_stringified)
        return
