import pika
import os
from dotenv import load_dotenv
load_dotenv()

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT'))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'admin')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'admin')

def get_connection():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    return pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST,port=RABBITMQ_PORT, credentials=credentials))

def create_channel(queue_name):
    print(RABBITMQ_HOST)
    print(RABBITMQ_PORT)
    print(RABBITMQ_USER)
    print(RABBITMQ_PASSWORD)
    connection = get_connection()
    channel = connection.channel()
    # Declare an exchange
    channel.exchange_declare(exchange="user_order", exchange_type='direct', durable=True)

    # Declare a queue
    channel.queue_declare(queue=queue_name, durable=True)

    # Bind the queue to the exchange with a routing key
    channel.queue_bind(exchange="user_order", queue=queue_name, routing_key=queue_name)

    return channel, connection
