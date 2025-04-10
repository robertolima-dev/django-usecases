#!/bin/bash

echo "📦 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "🛠️ Aplicando migrações..."
python manage.py migrate

# Executa baseado no modo
case "$1" in
  web)
    echo "🚀 Iniciando Daphne (ASGI)..."
    exec daphne -b 0.0.0.0 -p 8000 api_core.asgi:application
    ;;
  worker)
    echo "⚙️ Iniciando Celery Worker..."
    exec celery -A api_core worker --loglevel=info
    ;;
  beat)
    echo "⏰ Iniciando Celery Beat..."
    exec celery -A api_core beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    ;;
  *)
    echo "❌ Modo inválido. Use: web, worker ou beat"
    exit 1
    ;;
esac
