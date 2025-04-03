#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Start server"
gunicorn --preload --bind :8000 --workers 3 --timeout 900 api_core.wsgi:application