# Broken-Microservices 
## Project Overview

Broken-Microservices is a project designed to demonstrate the architecture and implementation of a microservices-based system. This project utilizes various technologies to build a robust and scalable system, including MongoDB for the database, Flask for the microservices, Kong for the API gateway, and RabbitMQ for the event-driven system.

## Architecture

The architecture of the Broken-Microservices project is composed of the following components:

- **MongoDB**: A NoSQL database used to store and manage data.
- **Flask**: A lightweight WSGI web application framework used to build the microservices.
- **Kong**: An API gateway that provides a single entry point for all the microservices, handling routing, authentication, and other API management tasks.
- **RabbitMQ**: A message broker that facilitates communication between the microservices in an event-driven manner.

![Architecture Diagram](docs/broken-microservices-arch.png)

## Project Directory Structure

The project directory structure is organized as follows:

```
.
├── aws
│   ├── broken-microservices.pem
│   ├── github_actions_id_rsa
│   └── github_actions_id_rsa.pub
├── docker-compose.yml
├── docs
│   ├── broken-microservices-arch.drawio
│   ├── broken-microservices-arch.png
│   ├── cloud-programming-assignment-2-report.pdf
│   ├── insomnia-testing-docs.json
│   ├── microservices_architecture.png
│   └── swagger
│       ├── order-service-html-documentation
│       │   └── index.html
│       ├── order-service-swagger.json
│       ├── order-swagger.yaml
│       ├── user-service-html-documentation
│       │   └── index.html
│       ├── user-service-swagger.json
│       └── user-swagger.yaml
├── LICENSE
├── README.md
├── src
│   ├── api_gateway
│   │   ├── docker-entrypoint.sh
│   │   ├── Dockerfile
│   │   ├── kong.conf
│   │   └── kong.yml
│   ├── __init__.py
│   ├── order_service
│   │   ├── app
│   │   │   ├── config.py
│   │   │   ├── events.py
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── __pycache__
│   │   │   │   ├── config.cpython-310.pyc
│   │   │   │   ├── events.cpython-310.pyc
│   │   │   │   ├── __init__.cpython-310.pyc
│   │   │   │   ├── models.cpython-310.pyc
│   │   │   │   └── routes.cpython-310.pyc
│   │   │   └── routes.py
│   │   ├── Dockerfile
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   └── wsgi.cpython-310.pyc
│   │   ├── requirements.txt
│   │   └── wsgi.py
│   ├── setup.py
│   ├── shared
│   │   ├── config
│   │   │   ├── __init__.py
│   │   │   ├── mongodb
│   │   │   │   ├── Dockerfile
│   │   │   │   ├── entrypoint.sh
│   │   │   │   ├── requirements.txt
│   │   │   │   ├── seed_database.py
│   │   │   │   └── setup_mongodb.py
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-310.pyc
│   │   │   │   └── rabbitmq_config.cpython-310.pyc
│   │   │   └── rabbitmq_config.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   └── __init__.cpython-310.pyc
│   │   └── schemas
│   │       ├── order_schema.json
│   │       └── user_schema.json
│   ├── user_service_v1
│   │   ├── app
│   │   │   ├── config.py
│   │   │   ├── events.py
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   └── routes.py
│   │   ├── Dockerfile
│   │   ├── __init__.py
│   │   ├── requirements.txt
│   │   └── wsgi.py
│   └── user_service_v2
│       ├── app
│       │   ├── config.py
│       │   ├── events.py
│       │   ├── __init__.py
│       │   ├── models.py
│       │   └── routes.py
│       ├── Dockerfile
│       ├── __init__.py
│       ├── requirements.txt
│       └── wsgi.py
└── tests
    ├── test_generate_diagram.py
    ├── test_mongodb_docker.py
    └── test_rabbitmq_exchange.py

22 directories, 73 files
```

## Running the Project

To run the Broken-Microservices project using Docker, follow these steps:

1. Ensure you have Docker installed on your Linux system.
2. Set the environment variables using the `.env.example` file as a template.
3. Execute the following command to build and run the Docker containers:

    ```bash
    docker compose down -v && docker compose build && docker compose up --force-recreate
    ```

This command will stop any running containers, build the images, and start the containers with the latest changes.

## Environment Variables

The project requires certain environment variables to be set for proper configuration. Use the `.env.example` file as a template to create your own `.env` file with the necessary values.

## Conclusion

The Broken-Microservices project showcases the implementation of a microservices architecture using modern technologies. By following the instructions provided, you can set up and run the project on your local machine, gaining insights into the workings of a microservices-based system.
