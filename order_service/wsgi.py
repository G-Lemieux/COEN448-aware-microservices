from app import create_app
from app.events import consume_user_update_events
import threading
import logging

app = create_app()

# Configure logging
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

def start_event_consumer():
    app.logger.info("Starting event consumer...")
    # with app.app_context():
    consume_user_update_events()

if __name__ == "__main__":
    print("Starting Order Service...", flush=True)
    app.logger.info("Order Service started")
    
    # Start the event consumer in a separate thread
    event_consumer_thread = threading.Thread(target=start_event_consumer, daemon=True)
    event_consumer_thread.start()
    
    app.run(debug=True)
    print("Order Service started", flush=True)