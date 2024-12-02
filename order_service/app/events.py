import json
from shared.config.rabbitmq_config import create_channel, get_connection
from flask import current_app
from app.models import api
import os
from dotenv import load_dotenv

load_dotenv()
QUEUE_NAME = os.getenv('RABBITMQ_QUEUE_NAME')

def consume_user_update_events():
    channel, connection = create_channel(QUEUE_NAME)

    def callback(ch, method, properties, body):
        event = json.loads(body)
        print(f"Received event: {event}")
        
        # Extract the data
        user_id = event['userId']
        emails = event.get('emails')
        delivery_address = event.get('deliveryAddress')

        print(event, flush=True)

        orders_collection = current_app.orders_collection
        old_orders = list(orders_collection.find({'userId': user_id}))
        if not old_orders:
            api.abort(404, "Order not found")
        
        update_fields = {}
        if emails:
            update_fields['emails'] = emails
        if delivery_address:
            update_fields['deliveryAddress'] = delivery_address

        for order in old_orders:
            orders_collection.update_one({'orderId': order["orderId"]}, {'$set': update_fields})
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    # Declare the queue (ensure it exists)
    queue_name = 'user_updates'
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange='user_order', queue=queue_name, routing_key=queue_name)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)
    print("Waiting for events...")
    channel.start_consuming()