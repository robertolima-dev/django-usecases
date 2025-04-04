#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Inicia o Daphne (ASGI)
daphne -b 0.0.0.0 -p 8000 api_core.asgi:application &

# Inicia o Celery Worker
celery -A api_core worker --loglevel=info &

# (Opcional) Inicia o Celery Beat
# celery -A api_core beat --loglevel=info &

# Fica em foreground para manter o container vivo
tail -f /dev/null