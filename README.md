### README v.1.0

# GitLab Gateway

## Описание

**GitLab Gateway** — это сервис для обработки вебхуков от GitLab, который декодирует информацию о событиях `merge request` и отправляет соответствующее сообщение в Telegram. Этот проект написан на FastAPI и использует асинхронные операции для обработки данных.

## Функциональные возможности

- Получение вебхуков от GitLab.
- Обработка данных о `merge request` событиях.
- Отправка уведомлений в Telegram с информацией о `merge request`.

## Установка и настройка

### Требования

- Python 3.11+
- Poetry

### Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/Rastorguev763/gitlab_webhook_gateway
    cd gitlab-gateway
    ```

2. Установите зависимости с помощью `poetry`:

    ```bash
    poetry install
    ```

    Если `poetry` не установлен сначала установите:

    ```bash
    pip install poetry
    ```

3. Активируйте виртуальное окружение, созданное `poetry`:

    ```bash
    poetry shell
    ```

### Настройка

1. Создайте файл `.env` в корневой директории проекта и добавьте в него переменные окружения:

    ```env
    MODE=DEV
    PRIVATE_TOKEN=your_gitlab_private_token
    BOT_TOKEN=your_telegram_bot_token
    SERVER_URL=https://your_server_url - используется для получения вебхуков от Telegram
    CHAT_ID=your_chat_id
    THREAD_ID=your_thread_id
    ```

    Базовые переменные находятся в `.env.template`

2. Настройте URL в настройках проекта для GitLab вебхуков на вашем сервере. Вебхук должен указывать на URL:

    ```url
    https://your_server_url/api/v1/webhook
    ```

## Запуск приложения

Для запуска приложения используйте следующую команду:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8050 --reload
```

Для получений вебхуков от Telegram на локальный компьютер нужно настроить туннелирование, например с помощь `ngrok` и прописать соответсвующий адрес в `SERVER_URL` `.env` файла.

## Запуск с помощью Docker Compose

После настройки `.env` файла конфигурации, выполните команду:

```bash
docker compose up -d
```

Docker создаст контейнер с приложением и установит все необходимые зависимости.
