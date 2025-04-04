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

    yield  # Run tests

    # Tear down Docker Compose
    # subprocess.run(
    #     ["docker", "compose", "-f", "docker-compose.test.yml", "down", "-v"],
    #     check=True
    # )

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

# Test: User Update


def test_user_update(api_base_url, mongo_client):
    # First create a user
    user_payload = {
        "firstName": "Update",
        "lastName": "Tester",
        "emails": ["update.test@example.com"],
        "deliveryAddress": {
            "street": "123 Test Street",
            "city": "Testville",
            "state": "Test State",
            "postalCode": "12345",
            "country": "Test Country"
        }
    }

    # Create user
    create_response = requests.post(
        f"{api_base_url}/users/",
        json=user_payload
    )

    assert create_response.status_code == 201
    created_user = create_response.json()
    user_id = created_user["userId"]

    # Update the user
    update_payload = {
        "emails": ["updated.email@example.com"],
        "deliveryAddress": {
            "street": "456 Update Street",
            "city": "Updateville",
            "state": "Update State",
            "postalCode": "54321",
            "country": "Update Country"
        }
    }

    # Send update request
    update_response = requests.put(
        f"{api_base_url}/users/{user_id}",
        json=update_payload
    )

    # Assertions for the response
    assert update_response.status_code == 200
    update_result = update_response.json()

    # The response should contain both old and new user data
    old_user = update_result[0]
    new_user = update_result[1]

    # Check old user data
    assert old_user["emails"] == ["update.test@example.com"]
    assert old_user["deliveryAddress"]["street"] == "123 Test Street"

    # Check new user data
    assert new_user["emails"] == ["updated.email@example.com"]
    assert new_user["deliveryAddress"]["street"] == "456 Update Street"
    assert new_user["deliveryAddress"]["city"] == "Updateville"

    # Verify update in MongoDB
    users_db = mongo_client[os.getenv("DATABASE_NAME")]
    users_collection = users_db["users"]
    updated_user = users_collection.find_one({"userId": user_id})
    assert updated_user is not None
    assert updated_user["emails"] == ["updated.email@example.com"]
    assert updated_user["deliveryAddress"]["street"] == "456 Update Street"

# Test: Order Creation


def test_order_creation(api_base_url, mongo_client):
    # Create a new user
    user_payload = {
        "firstName": "Order-Creation",
        "lastName": "Tester",
        "emails": ["oc.test@example.com"],
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

    # User Creation Assertions
    assert response.status_code == 201
    created_user = response.json()
    assert created_user['firstName'] == "Order-Creation"
    assert created_user['lastName'] == "Tester"
    user_id = created_user["userId"]

    # Verify user in MongoDB
    users_db = mongo_client[os.getenv("DATABASE_NAME")]
    users_collection = users_db["users"]
    user = users_collection.find_one({"userId": user_id})
    assert user is not None
    assert user["emails"] == ["oc.test@example.com"]

    # Create an Order
    order_payload = {
        "items": [{
            "itemId": "item1",
            "quantity": 1,
            "price": 4.99
        }],
        "userEmails": ["oc.test@example.com"],
        "deliveryAddress": {
            "street": "123 Test Street",
            "city": "Testville",
            "state": "Test State",
            "postalCode": "12345",
            "country": "Test Country"
        },
        "orderStatus": "under process"
    }

    # Send Order Creation Request
    response = requests.post(
        f"{api_base_url}/orders/",
        json=order_payload
    )

    # Assertions
    assert response.status_code == 201
    created_order = response.json()
    assert created_order['orderStatus'] == "under process"
    order_id = created_order["orderId"]

    # Verify Order in MongoDB
    orders_db = mongo_client[os.getenv("DATABASE_NAME")]
    orders_collection = orders_db["orders"]
    created_order = orders_collection.find_one({"orderId": order_id})
    assert created_order is not None
    assert created_order["userEmails"] == ["oc.test@example.com"]
    assert created_order["deliveryAddress"]["street"] == "123 Test Street"

# Test: Get Order Status


def test_retrieve_orders_by_status(api_base_url):
    order_payload = []

    # Create a new user
    first_user_payload = {
        "firstName": "First Order",
        "lastName": "User",
        "emails": ["number.one@example.com"],
        "deliveryAddress": {
            "street": "745 Main Street",
            "city": "Testville",
            "state": "Test State",
            "postalCode": "54321",
            "country": "Test Country"
        }
    }

    # Create a second new user
    second_user_payload = {
        "firstName": "Second Order",
        "lastName": "Tester",
        "emails": ["numer.two@example.com"],
        "deliveryAddress": {
            "street": "748 Main Street",
            "city": "Testville",
            "state": "Test State",
            "postalCode": "54321",
            "country": "Test Country"
        }
    }

    # Send user creation request
    response1 = requests.post(
        f"{api_base_url}/users/",
        json=first_user_payload
    )
    response2 = requests.post(
        f"{api_base_url}/users/",
        json=second_user_payload
    )
    assert response1.status_code == 201
    assert response2.status_code == 201

    # Create an Order
    order_payload.append({
        "items": [{
            "itemId": "item1",
            "quantity": 1,
            "price": 4.99
        }],
        "userEmails": ["number.one@example.com"],
        "deliveryAddress": {
            "street": "745 Main Street",
            "city": "Testville",
            "state": "Test State",
            "postalCode": "54321",
            "country": "Test Country"
        },
        "orderStatus": "under process"
    })

    # Create a Second Order
    order_payload.append({
        "items": [{
            "itemId": "item2",
            "quantity": 3,
            "price": 9.98
        }],
        "userEmails": ["number.two@example.com"],
        "deliveryAddress": {
            "street": "748 Main Street",
            "city": "Testville",
            "state": "Test State",
            "postalCode": "54321",
            "country": "Test Country"
        },
        "orderStatus": "shipping"
    })

    # Create a third Order
    order_payload.append({
        "items": [{
            "itemId": "item3",
            "quantity": 9,
            "price": 24.78
        }],
        "userEmails": ["number.one@example.com"],
        "deliveryAddress": {
            "street": "745 Main Street",
            "city": "Testville",
            "state": "Test State",
            "postalCode": "54321",
            "country": "Test Country"
        },
        "orderStatus": "delivered"
    })

    # Create an Order
    order_payload.append({
        "items": [{
            "itemId": "item4",
            "quantity": 1,
            "price": 36.99
        }],
        "userEmails": ["number.two@example.com"],
        "deliveryAddress": {
            "street": "748 Main Street",
            "city": "Testville",
            "state": "Test State",
            "postalCode": "54321",
            "country": "Test Country"
        },
        "orderStatus": "under process"
    })

    responses = []

    for payload in order_payload:
        responses.append(requests.post(
            f"{api_base_url}/orders/",
            json=payload
        ))

    for response in responses:
        assert response.status_code == 201

    get_response_under_process = requests.get(
        f"{api_base_url}/orders/", {"status": "under process"}
    )
    assert get_response_under_process.status_code == 200
    response_data = get_response_under_process.json()
    assert isinstance(
        response_data, list), f"Expected a list, but received a {type(response_data)}"
    assert len(response_data) > 0, "Returned an empty list."
    for item in response_data:
        assert isinstance(
            item, dict), f"Expected a dictionary, but got {type(item)}"
        assert 'orderStatus' in item
        assert item["orderStatus"] == "under process"

# Test: Update Order Status


def test_update_order_status(api_base_url, mongo_client):
    # Create an order
    order_payload = {
        "items": [{
            "itemId": "item2",
            "quantity": 5,
            "price": 27.94
        }],
        "userEmails": ["verification@example.com"],
        "deliveryAddress": {
            "street": "205 Main Street",
            "city": "Testville",
            "state": "Test State",
            "postalCode": "54321",
            "country": "Test Country"
        },
        "orderStatus": "under process"
    }

    response = requests.post(
        f"{api_base_url}/orders/",
        json=order_payload
    )
    assert response.status_code == 201, f"Failed to create order."
    new_order = response.json()
    order_id = new_order["orderId"]

    # Create new Status
    update_payload = {"orderStatus": "shipping"}

    update_response = requests.put(
        f"{api_base_url}/orders/{order_id}/status",
        json=update_payload
    )
    assert update_response.status_code == 200, f"Expected code 201, received: {update_response.status_code}"

# Test: Update Order Details


def test_update_order_details(api_base_url, mongo_client):
    # Create an order
    order_payload = {
        "items": [{
            "itemId": "item3",
            "quantity": 4,
            "price": 45.95
        }],
        "userEmails": ["verification@example.com"],
        "deliveryAddress": {
            "street": "205 Main Street",
            "city": "Testville",
            "state": "Test State",
            "postalCode": "54321",
            "country": "Test Country"
        },
        "orderStatus": "shipping"
    }

    response = requests.post(
        f"{api_base_url}/orders/",
        json=order_payload
    )
    assert response.status_code == 201, f"Failed to create order."
    new_order = response.json()
    order_id = new_order["orderId"]

    # Create new Status
    update_payload = {
        "userEmails": ["new.address@example.com", "verification@example.com"],
        "deliveryAddress": {
            "street": "95 North Blvd",
            "city": "Quality",
            "state": "Test State",
            "postalCode": "65421",
            "country": "Test Country"
        }
    }

    update_response = requests.put(
        f"{api_base_url}/orders/{order_id}/details",
        json=update_payload
    )
    assert update_response.status_code == 200, f"Expected code 201, received: {update_response.status_code}"


# Test: Update Propagation


def test_update_propagation(api_base_url, mongo_client):
    # Create a User
    user_payload = {
        "firstName": "Jim",
        "lastName": "Bob",
        "emails": ["propagation.test@example.com"],
        "deliveryAddress": {
            "street": "56 Main Street",
            "city": "Testville",
            "state": "Test State",
            "postalCode": "12345",
            "country": "Test Country"
        }
    }
    new_user_response = requests.post(
        f"{api_base_url}/users/",
        json=user_payload
    )
    assert new_user_response.status_code == 201, f"Failed to create New User: Code: {new_user_response.status_code}"
    created_user = new_user_response.json()
    user_id = created_user["userId"]

    # Create an Order
    order_payload = {
        "items": [{
            "itemId": "item3",
            "quantity": 6,
            "price": 36.99
        }],
        "userEmails": ["propagation.test@example.com"],
        "deliveryAddress": {
            "street": "56 Main Street",
            "city": "Testville",
            "state": "Test State",
            "postalCode": "12345",
            "country": "Test Country"
        },
        "orderStatus": "under process",
        "userId": user_id
    }
    new_order_response = requests.post(
        f"{api_base_url}/orders/",
        json=order_payload
    )
    assert new_order_response.status_code == 201, f"Failed to create New Order: Code: {new_order_response.status_code}"
    new_order = new_order_response.json()
    order_id = new_order["orderId"]

    # Update User
    update_payload = {
        "emails": ["prop.update@example.com"],
        "deliveryAddress": {
            "street": "123 North Blvd",
            "city": "Updateville",
            "state": "Update State",
            "postalCode": "54321",
            "country": "Update Country"
        }
    }

    # Send update request
    update_response = requests.put(
        f"{api_base_url}/users/{user_id}",
        json=update_payload
    )

    # Assertions for the response
    assert update_response.status_code == 200, f"Failed to Update the User: Code: {update_response.status_code}"
    update_result = update_response.json()

    # The response should contain both old and new user data
    new_user = update_result[1]
    # Check new user data
    assert new_user["emails"] == ["prop.update@example.com"]
    assert new_user["deliveryAddress"]["street"] == "123 North Blvd"
    assert new_user["deliveryAddress"]["city"] == "Updateville"

    # Verify update in MongoDB
    orders_db = mongo_client[os.getenv("DATABASE_NAME")]
    orders_collection = orders_db["orders"]
    updated_order = orders_collection.find_one({"orderId": order_id})
    assert updated_order is not None
    assert updated_order["userEmails"] == ["prop.update@example.com"]
    assert updated_order["deliveryAddress"]["street"] == "123 North Blvd"
    assert updated_order["userId"] == user_id
