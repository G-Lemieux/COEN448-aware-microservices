from flask import Flask
from flask_restx import Api
from order_service.app.routes import api as order_api
from pymongo import MongoClient
from order_service.app.events import consume_user_update_events
import threading

def start_event_consumer(app: Flask):
    print("Starting event consumer...")
    with app.app_context():
        consume_user_update_events()

def create_app():
    app = Flask(__name__)
    app.config.from_object('order_service.app.config.Config')
    api = Api(app)
    api.add_namespace(order_api, path='/orders')
    
    # Initialize MongoDB client
    print ("Connecting to MongoDB... ", app.config['MONGO_URI'])
    mongo_client = MongoClient(app.config['MONGO_URI'])
    app.mongo_client = mongo_client
    app.db = mongo_client[app.config['DATABASE_NAME']]
    app.orders_collection = app.db['orders']

    # Start the event consumer in a separate thread
    event_consumer_thread = threading.Thread(target=start_event_consumer, args=(app,), daemon=True)
    event_consumer_thread.start()
        
    return app