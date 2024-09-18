import json
import pika
import pika.adapters.blocking_connection
import pika.credentials
from src.infra.consumer_handler import ConsumerHandler
from src.schemas import InvalidSchemaException


class Consumer:
    def __init__(
        self,
        queue_name: str,
        consumer_handler: ConsumerHandler,
        channel: pika.adapters.blocking_connection.BlockingChannel,
    ):
        self.queue_name = queue_name
        self.consumer_handler = consumer_handler
        self.channel = channel

    def consumer_callback(self, channel, method_frame, header_frame, body):
        try:
            body_json_data = json.loads(body.decode("utf-8"))
            print(f'[RabbitMQConsumer] request_id: {body_json_data["request_id"]} '.ljust(75, '-'))
        except Exception as json_exception:
            print(
                f"[RabbitMQConsumer] The message body is not a valid JSON, rejecting message: {json_exception}"
            )
            self.channel.basic_nack(
                delivery_tag=method_frame.delivery_tag, requeue=False
            )
            return

        try:
            self.consumer_handler.handle(body_json_data)
            
            print("[RabbitMQConsumer] Acknowledging the processed message")
            self.channel.basic_ack(method_frame.delivery_tag)
        except InvalidSchemaException:
            print(
                f"[RabbitMQConsumer] Error validating message body schema, rejecting message without requeue"
            )
            self.channel.basic_reject(method_frame.delivery_tag, False)
        except Exception as e:
            print(f"[RabbitMQConsumer] Error processing message {e}")
            self.channel.basic_nack(method_frame.delivery_tag)

    def prepare(self):
        print(f"[RabbitMQConsumer] Preparing queue consumer: {self.queue_name}")
        self.channel.basic_consume(self.queue_name, self.consumer_callback)
        return
