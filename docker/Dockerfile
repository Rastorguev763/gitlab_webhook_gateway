FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Обновляем и устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y \
    python3-dev \
    gcc \
    libc-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Обновляем pip и устанавливаем Poetry
RUN pip install --upgrade pip setuptools
RUN pip install poetry

WORKDIR /usr/src/app
COPY ./requirements.txt ./
COPY ./.env ./
COPY ./src/ ./src
COPY ./migrations/ ./migrations
COPY ./alembic.ini ./
COPY pyproject.toml ./
RUN poetry install
COPY ./docker/start.sh ./start.sh
RUN chmod 777 start.sh