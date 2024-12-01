#!/bin/bash
set -e

# Start MongoDB
mongod --bind_ip_all --logpath /var/log/mongodb.log --dbpath /data/db &

# Wait for MongoDB to be ready
for i in {1..30}; do
    if mongo --host 0.0.0.0:27017 --eval "db.adminCommand('ping')" > /dev/null 2>&1; then
        echo "MongoDB is ready!"
        break
    fi
    echo "Waiting for MongoDB to start... ($i)"
    sleep 5
done

# Exit if MongoDB is not ready after the timeout
if ! mongo --host 0.0.0.0:27017 --eval "db.adminCommand('ping')" > /dev/null 2>&1; then
    echo "MongoDB failed to start."
    exit 1
fi

# Run the setup and seed scripts
echo "Running setup script..."
python3 /app/setup_mongodb.py

echo "Running seed script..."
python3 /app/seed_database.py

# Keep MongoDB running
wait
