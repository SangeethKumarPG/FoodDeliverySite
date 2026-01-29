#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting Entrypoint Script..."

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn or development server
# For production (Dokploy), Gunicorn is recommended.
# If Gunicorn is in requirements.txt, use it.
if pip show gunicorn > /dev/null 2>&1; then
    echo "Starting Gunicorn..."
    exec gunicorn savourelle_project.wsgi:application --bind 0.0.0.0:8000 --workers 3
else
    echo "Gunicorn not found, starting development server..."
    exec python manage.py runserver 0.0.0.0:8000
fi
