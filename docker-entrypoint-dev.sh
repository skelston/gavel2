#!/bin/bash
set -e

# Function to wait for PostgreSQL using Python (no psql needed)
wait_for_postgres() {
    until python -c "
import os
import psycopg2
from psycopg2 import OperationalError
import time

try:
    conn = psycopg2.connect(
        dbname=os.environ.get('POSTGRES_DB', 'postgres'),
        user=os.environ.get('POSTGRES_USER', 'postgres'),
        password=os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        host='postgres',
        connect_timeout=3
    )
    conn.close()
    print('Postgres is up - continuing')
    exit(0)
except OperationalError as e:
    print(f'Postgres is unavailable - {e}')
    time.sleep(1)
    exit(1)
"
    do
        sleep 1
    done
}

# Wait for the database
wait_for_postgres

# Initialize database if needed
if [ ! -f .db-initialized ]; then
    echo "Initializing database..."
    python initialize.py
    touch .db-initialized
    echo "Database initialized."
fi

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn -c workers.py gavel:app