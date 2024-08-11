# __init__.py
from aiogram import Router

from telegram_bot.routers import base_commad_tg_route

main_router = Router()

main_router.include_routers(
    base_commad_tg_route.router,
)
