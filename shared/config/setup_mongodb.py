"""
This script sets up MongoDB collections for a microservices architecture.
It initializes the 'users' and 'orders' collections with appropriate schema validation.

Functions:
    setup_users_collection(): Initializes the 'users' collection with schema validation.
    setup_orders_collection(): Initializes the 'orders' collection with schema validation.
    main(): Main function to set up the MongoDB collections.

Author:
    @TheBarzani
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Retrieve MongoDB credentials from .env
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

if not MONGO_URI or not DATABASE_NAME:
    raise ValueError("MongoDB URI or database name is not set in the .env file.")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# Initialize Users Collection
def setup_users_collection():
    """
    Sets up the 'users' collection in the MongoDB database with a JSON schema validator.

    The schema enforces the following structure:
    - userId: string (required)
    - emails: array of strings (required, each string must match the email pattern)
    - deliveryAddress: object (required) with the following properties:
        - street: string (required)
        - city: string (required)
        - state: string (required)
        - postalCode: string (required)
        - country: string (required)
    - phoneNumber: string (optional, must match the pattern for phone numbers with 10 to 15 digits)
    - createdAt: date (optional)
    - updatedAt: date (optional)

    If the collection already exists or creation fails, an exception is caught and an error message is printed.
    Raises:
        Exception: If the collection creation fails for any reason other than it already existing.
    """
    
    try:
        db.create_collection("users", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["userId", "emails", "deliveryAddress"],
                "properties": {
                    "userId": {"bsonType": "string"},
                    "emails": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "string",
                            "pattern": "^.+@.+\\..+$"
                        }
                    },
                    "deliveryAddress": {
                        "bsonType": "object",
                        "required": ["street", "city", "state", "postalCode", "country"],
                        "properties": {
                            "street": {"bsonType": "string"},
                            "city": {"bsonType": "string"},
                            "state": {"bsonType": "string"},
                            "postalCode": {"bsonType": "string"},
                            "country": {"bsonType": "string"}
                        }
                    },
                    "phoneNumber": {"bsonType": "string", "pattern": "^[0-9]{10,15}$"},
                    "createdAt": {"bsonType": "date"},
                    "updatedAt": {"bsonType": "date"}
                }
            }
        })
        print("Users collection created successfully.")
    except Exception as e:
        print(f"Users collection already exists or failed: {e}")

# Initialize Orders Collection
def setup_orders_collection():
    """
    Sets up the 'orders' collection in MongoDB with a JSON schema validator.

    The schema for the 'orders' collection includes the following fields:
    - orderId (string): Unique identifier for the order.
    - items (array of objects): List of items in the order, each containing:
        - itemId (string): Unique identifier for the item.
        - name (string): Name of the item.
        - quantity (int): Quantity of the item, must be at least 1.
        - price (double): Price of the item, must be at least 0.
    - userEmails (array of strings): List of user email addresses, each must match the email pattern.
    - deliveryAddress (object): Delivery address containing:
        - street (string): Street address.
        - city (string): City name.
        - state (string): State name.
        - postalCode (string): Postal code.
        - country (string): Country name.
    - orderStatus (string): Status of the order, must be one of ["under process", "shipping", "delivered"].
    - createdAt (date): Date when the order was created.
    - updatedAt (date): Date when the order was last updated.

    If the collection already exists or creation fails, an exception is caught and an error message is printed.
    """

    try:
        db.create_collection("orders", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["orderId", "items", "userEmails", "deliveryAddress", "orderStatus"],
                "properties": {
                    "orderId": {"bsonType": "string"},
                    "items": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "object",
                            "required": ["itemId", "quantity", "price"],
                            "properties": {
                                "itemId": {"bsonType": "string"},
                                "name": {"bsonType": "string"},
                                "quantity": {"bsonType": "int", "minimum": 1},
                                "price": {"bsonType": "double", "minimum": 0}
                            }
                        }
                    },
                    "userEmails": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "string",
                            "pattern": "^.+@.+\\..+$"
                        }
                    },
                    "deliveryAddress": {
                        "bsonType": "object",
                        "required": ["street", "city", "state", "postalCode", "country"],
                        "properties": {
                            "street": {"bsonType": "string"},
                            "city": {"bsonType": "string"},
                            "state": {"bsonType": "string"},
                            "postalCode": {"bsonType": "string"},
                            "country": {"bsonType": "string"}
                        }
                    },
                    "orderStatus": {"bsonType": "string", "enum": ["under process", "shipping", "delivered"]},
                    "createdAt": {"bsonType": "date"},
                    "updatedAt": {"bsonType": "date"}
                }
            }
        })
        print("Orders collection created successfully.")
    except Exception as e:
        print(f"Orders collection already exists or failed: {e}")

# Main function to set up the database
def main():
    print("Setting up MongoDB...")
    setup_users_collection()
    setup_orders_collection()
    print("MongoDB setup complete.")

if __name__ == "__main__":
    main()
