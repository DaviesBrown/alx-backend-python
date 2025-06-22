#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status

# Wait for the database
/usr/local/bin/wait-for-it.sh db 3306 -- echo "Database is up!"

# Run Django migrations
echo "Running Django migrations..."
python manage.py migrate --noinput

# Start the Django development server
echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000