#!/bin/sh

# Применяем миграции
alembic upgrade head

# Запускаем приложение (используем порт из переменной Render $PORT)
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}