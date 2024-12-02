# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python scripts and .env file
COPY setup_mongodb.py /app
COPY seed_database.py /app
COPY .env /app
COPY entrypoint.sh /app

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Set the entrypoint to the shell script
ENTRYPOINT ["/app/entrypoint.sh"]