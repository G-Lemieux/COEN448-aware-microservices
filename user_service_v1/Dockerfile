# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt



# Define environment variables
ENV FLASK_APP=user_service_v1.wsgi
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Make port running flask available to the world outside this container
EXPOSE ${FLASK_RUN_PORT}

# Run the application
CMD ["flask", "run"]