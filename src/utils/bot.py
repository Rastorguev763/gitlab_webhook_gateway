from src.telegram_bot.bot_main import bot


async def send_telegram_message(chat_id: int, message: str, thread_id: int = None):
    """Асинхронная функция для отправки сообщения через Telegram бота."""
    if thread_id:
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            message_thread_id=thread_id,
            disable_web_page_preview=True,
        )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            disable_web_page_preview=True,
        )
