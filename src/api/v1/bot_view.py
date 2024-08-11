import asyncio
from aiogram import types
from fastapi import FastAPI, APIRouter
import aiogram

from core.settings import settings
from telegram_bot.bot_main import dp, bot

WEBHOOK_URL = f"{settings.SERVER_URL}/api/v1/bot/{settings.BOT_TOKEN}"

# Создаем корневое приложение FastAPI
app = FastAPI()

# Создаем роутер
router = APIRouter()


async def set_webhook_with_retry(bot, webhook_url, retries=5, initial_delay=1):
    delay = initial_delay
    for attempt in range(retries):
        try:
            await bot.set_webhook(url=webhook_url)
            return
        except aiogram.exceptions.TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
        except Exception:
            await asyncio.sleep(delay)
            delay *= 2


@app.on_event("startup")
async def on_startup() -> None:
    print(f"WEBHOOK_URL: {WEBHOOK_URL}")
    """Обработчик события 'startup' для FastAPI."""
    # Получаем информацию о текущем вебхуке бота
    try:
        webhook_info = await bot.get_webhook_info()

        # Если URL вебхука не совпадает с ожидаемым URL, устанавливаем вебхук
        if webhook_info.url != WEBHOOK_URL:
            await set_webhook_with_retry(bot, WEBHOOK_URL)
    except Exception as e:
        print(f"Failed to set webhook: {e}")


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """Обработчик события 'shutdown' для FastAPI."""
    # Закрываем сеанс бота при завершении работы
    await bot.session.close()


@router.post(f"/{settings.BOT_TOKEN}")
async def bot_webhook(update: dict) -> None:
    """Обработчик HTTP POST-запросов для вебхука бота."""
    # Преобразуем JSON-обновление в объект types.Update
    telegram_update = types.Update(**update)

    # Передаем обновление боту для обработки
    await dp.feed_update(bot=bot, update=telegram_update)


# Включаем роутер в основное приложение
app.include_router(router)
