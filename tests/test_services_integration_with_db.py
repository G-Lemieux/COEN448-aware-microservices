import os
import pytest
import requests
import pymongo
import pika
import subprocess
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fixture to manage Docker Compose
@pytest.fixture(scope="module", autouse=True)
def docker_compose():
    # Start Docker Compose
    subprocess.run(
        ["docker", "compose", "-f", "docker-compose.test.yml", "up", "--build", "-d"],
        check=True
    )
    
    # Wait for services to be ready
    wait_for_service("http://localhost:8001/")
    # wait_for_service("http://localhost:15672")  # RabbitMQ management UI
    
    yield  # Run tests
    
    # Tear down Docker Compose
    subprocess.run(
        ["docker", "compose", "-f", "docker-compose.test.yml", "down", "-v"],
        check=True
    )

# Helper function to wait for service readiness
def wait_for_service(url, timeout=200):
    start = time.time()
    while time.time() - start < timeout:
        try:
            if requests.get(url).status_code == 200:
                return
        except Exception:
            time.sleep(1)
    raise TimeoutError(f"Service at {url} not ready")

# Fixture for API base URL
@pytest.fixture(scope="module")
def api_base_url():
    return "http://localhost:8000"

# Fixture for MongoDB client
@pytest.fixture(scope="module")
def mongo_client():
    client = pymongo.MongoClient(
        host="localhost", 
        port=27017,
        username=os.getenv("MONGO_USERNAME"),
        password=os.getenv("MONGO_PASSWORD"),
        authSource="admin"
        )
    yield client
    client.close()

# # Fixture for RabbitMQ connection
# @pytest.fixture(scope="module")
# def rabbitmq_connection():
#     connection = pika.BlockingConnection(
#         pika.ConnectionParameters("localhost", 5673)
#     )
#     yield connection
#     connection.close()

# Test: User Creation
def test_user_creation(api_base_url, mongo_client):
    # Create a new user
    user_payload = {
        "firstName": "Integration",
        "lastName": "Tester",
        "emails": ["integration.test@example.com"],
        "deliveryAddress": {
            "street": "123 Test Street",
            "city": "Testville",
            "state": "Test State",
            "postalCode": "12345",
            "country": "Test Country"
        }
    }
    
    # Send user creation request
    response = requests.post(
        f"{api_base_url}/users/", 
        json=user_payload
    )
    
    # Assertions
    assert response.status_code == 201
    created_user = response.json()
    assert created_user['firstName'] == "Integration"
    assert created_user['lastName'] == "Tester"
    
    # Verify user in MongoDB
    users_db = mongo_client[os.getenv("DATABASE_NAME")]
    users_collection = users_db["users"]
    user = users_collection.find_one({"userId": created_user["userId"]})
    assert user is not None
    assert user["emails"] == ["integration.test@example.com"]

# # Test: Order Creation
# def test_order_creation(api_base_url, rabbitmq_connection):
#     # Create an order
#     order_payload = {
#         "userId": "test-user-id",
#         "items": [
#             {
#                 "itemId": "test-item-001",
#                 "quantity": 2,
#                 "price": 29.99
#             }
#         ],
#         "userEmails": ["test@example.com"],
#         "deliveryAddress": {
#             "street": "456 Order Street",
#             "city": "Ordertown",
#             "state": "Order State",
#             "postalCode": "54321",
#             "country": "Order Country"
#         },
#         "orderStatus": "under process"
#     }
    
#     # Send order creation request
#     response = requests.post(
#         f"{api_base_url}/orders/", 
#         json=order_payload
#     )
    
#     # Assertions
#     assert response.status_code == 201
#     created_order = response.json()
#     assert created_order['orderStatus'] == "under process"
    
#     # Verify RabbitMQ message
#     channel = rabbitmq_connection.channel()
#     method_frame, _, body = channel.basic_get("order_queue")
#     assert method_frame is not None  # Message exists
#     assert b"test-user-id" in body  # Verify message content

# Test: User Update Synchronization
def test_user_update_synchronization(api_base_url, mongo_client):
    # Create a user first
    user_payload = {
        "firstName": "Initial",
        "lastName": "User",
        "emails": ["initial.user@example.com"],
        "deliveryAddress": {
            "street": "123 Initial Street",
            "city": "Initial City",
            "state": "Initial State",
            "postalCode": "12345",
            "country": "Initial Country"
        }
    }
    create_response = requests.post(f"{api_base_url}/users/", json=user_payload)
    user_id = create_response.json()["userId"]
    print(f"Created user with ID: {user_id}")
    
    # Prepare user update payload
    update_payload = {
        "emails": ["updated.email@example.com"],
        "deliveryAddress": {
            "street": "789 Updated Street",
            "city": "Updatedville",
            "state": "Updated State",
            "postalCode": "67890",
            "country": "Updated Country"
        }
    }
    
    # Perform user update
    update_response = requests.put(
        f"{api_base_url}/users/{user_id}", 
        json=update_payload
    )
    
    # Assertions
    assert update_response.status_code == 200
    
    # Verify update in MongoDB
    users_db = mongo_client[os.getenv("DATABASE_NAME")]
    users_collection = users_db["users"]
    updated_user = users_collection.find_one({"userId": user_id})
    assert updated_user is not None
    assert updated_user['emails'] == ["updated.email@example.com"]
    assert updated_user['deliveryAddress']['street'] == "789 Updated Street"
    
    # Cleanup
    users_collection.delete_one({"userId": user_id})