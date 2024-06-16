# Setup Instructions
Prerequisites
    Docker
    Docker Compose

# Setting up the Environment Variables
    Navigate to the HealthTracker directory:
    cd HealthTracker


# Create a .env file in the root directory of the project with the following content:
    SECRET_KEY=django-insecure-$*w21uu^bk^*9os36q&a=7rde-izkmpef9x+_d_vj6may2b5q&
    DEBUG=TRUE
    POSTGRES_DB=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    HOST=5432

# Running the Project
  docker compose -f docker-compose.dev.yml up -d


# Accessing the Documentation
  http://127.0.0.1:8000/api/schema/docs/
