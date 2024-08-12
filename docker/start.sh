#!/bin/sh
echo "Run migrations..."

alembic upgrade head

echo "End migrations..."

gunicorn src.main:app --bind=0.0.0.0:8050  --workers 4 --worker-class uvicorn.workers.UvicornWorker