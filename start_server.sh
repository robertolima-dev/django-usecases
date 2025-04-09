#!/bin/bash

echo "📦 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "🛠️ Aplicando migrações..."
python manage.py migrate

echo "🚀 Iniciando Daphne (ASGI)..."
daphne -b 0.0.0.0 -p 8000 api_core.asgi:application &

echo "⚙️ Iniciando Celery Worker..."
celery -A api_core worker --loglevel=info &

echo "⏰ Iniciando Celery Beat..."
celery -A api_core beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler &

# Mantém o container vivo
tail -f /dev/null
