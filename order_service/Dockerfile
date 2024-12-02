# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY order_service/ /app
COPY shared/config/rabbitmq_config.py /app/shared/config/
COPY shared/config/__init__.py /app/shared/config/
COPY shared/__init__.py /app/shared/


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variables
ENV FLASK_APP=wsgi
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV RABBITMQ_HOST=${RABBITMQ_HOST}
ENV RABBITMQ_PORT=${RABBITMQ_PORT}
ENV RABBITMQ_USER=${RABBITMQ_ORDER_USER}
ENV RABBITMQ_PASSWORD=${RABBITMQ_ORDER_PASSWORD}
ENV RABBITMQ_QUEUE_NAME=${RABBITMQ_QUEUE_NAME}

# Make port running flask available to the world outside this container
EXPOSE 5000

# Run the application
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "--log-level=error", "wsgi:app"]