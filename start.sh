#!/bin/bash



# Запуск Uvicorn
exec uvicorn server.server:app --host 0.0.0.0 --port 8000 &

# Запуск Celery
exec celery -A server.config.celery_app worker --loglevel=info
