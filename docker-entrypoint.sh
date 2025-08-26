#!/bin/bash
set -e

# Function to wait for PostgreSQL to be ready (highly recommended)
wait_for_postgres() {
    until PGPASSWORD=$POSTGRES_PASSWORD psql -h "postgres" -U "postgres" -d "postgres" -c '\q'; do
        >&2 echo "Postgres is unavailable - sleeping"
        sleep 1
    done
    >&2 echo "Postgres is up - continuing"
}

# Wait for the database (comment out if not using Postgres in this setup)
wait_for_postgres

# Initialize the database if it hasn't been done yet.
# This simple check creates a flag file after first init.
if [ ! -f .db-initialized ]; then
    echo "Initializing database..."
    python initialize.py
    touch .db-initialized
    echo "Database initialized."
fi

# Start Gunicorn to serve the application using the config file.
echo "Starting Gunicorn..."
exec gunicorn -c workers.py gavel:app