import pika
import json

RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "notifications"

def publish_message(message: dict):
    """
    Публикует сообщение в очередь RabbitMQ.
    :param message: Словарь с данными сообщения.
    """
    try:
        parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=5672)
        with pika.BlockingConnection(parameters) as conn:
            with conn.channel() as ch:
                ch.queue_declare(queue=QUEUE_NAME)

                ch.basic_publish(exchange='', routing_key=QUEUE_NAME, body=json.dumps(message))

                print(f"[RabbitMQ] Sent: {message}")

    except Exception as e:
        print(f"[RabbitMQ] Error while publishing message: {e}")
