# Docker Containerization for Messaging App

This directory contains Docker configuration files for containerizing the Django messaging application.

## Files

- `Dockerfile` - Docker image configuration for the Django app
- `docker-compose.yml` - Multi-container orchestration with MySQL database
- `requirements.txt` - Python dependencies
- `.dockerignore` - Files to exclude from Docker build
- `.env.example` - Example environment variables (copy to .env)

## Setup Instructions

### Prerequisites
- Docker installed
- Docker Compose installed

### Environment Setup

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your own values (DO NOT commit this file)

### Building and Running

#### Task 0: Single Container
```bash
# Build the Docker image
docker build -t messaging-app .

# Run the container
docker run -p 8000:8000 messaging-app
```

#### Task 1 & 2: Multi-Container with Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Database Configuration

The app is configured to use MySQL in Docker with:
- Database: messaging_db
- User: messaging_user
- Password: Set in .env file
- Host: db (Docker service name)
- Port: 3306

## Volumes

The `mysql_data` volume persists database data across container restarts.

## Access

- Django App: http://localhost:8000
- MySQL: localhost:3306

## Migrations

Migrations run automatically when starting with docker-compose. To run manually:
```bash
docker-compose exec web python manage.py migrate
```

## Creating Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```
