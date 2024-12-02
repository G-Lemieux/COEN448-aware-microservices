from order_service.app import create_app
import threading

app = create_app()

if __name__ == "__main__":
    print("Starting Order Service...")
    
    app.run(debug=True)
    
    print("Order Service started")