import time

import pika
from pika import exceptions
from notifications import process_notification

RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "notifications"


def callback(ch, method, properties, body):
    process_notification(body)


def start_consumer():
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=5672)

    while True:
        try:
            print(f"Connecting to RabbitMQ...")

            with pika.BlockingConnection(parameters) as conn:
                with conn.channel() as ch:
                    ch.queue_declare(queue=QUEUE_NAME)

                    ch.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
                    print("Waiting for messages. To exit press CTRL+C")

                    ch.start_consuming()
        except exceptions.AMQPConnectionError:
            print("RabbitMQ is not available. Retrying in 3 seconds...")
            time.sleep(3)
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
