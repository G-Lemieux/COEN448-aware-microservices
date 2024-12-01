# Start with the official MongoDB image
FROM mongo:latest

# Install Python and necessary libraries
RUN apt-get update && apt-get install -y python3 python3-pip && apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy the Python scripts and .env file from the parent directory
COPY shared/config/setup_mongodb.py shared/config/seed_database.py shared/config/.env /app/

# Install Python dependencies
RUN pip3 install pymongo python-dotenv

# Copy entrypoint script
COPY shared/config/mongodb/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Use the custom entrypoint script
ENTRYPOINT ["docker-entrypoint.sh"]
