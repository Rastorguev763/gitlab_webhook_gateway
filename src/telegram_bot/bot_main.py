# bot_main.py

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.core.settings import settings
from src.telegram_bot.routers import main_router

# Создаем экземпляр бота с использованием токена из конфигурации
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Создаем диспетчер (Dispatcher) для обработки сообщений и событий бота
dp = Dispatcher(bot=bot)
dp.include_router(main_router)
