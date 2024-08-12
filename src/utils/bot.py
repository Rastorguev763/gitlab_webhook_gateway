from src.telegram_bot.bot_main import bot


async def send_telegram_message(
    chat_id: int, message: str, thread_id: int = None, reply_to_message_id: int = None
):
    """Асинхронная функция для отправки сообщения через Telegram бота."""
    if thread_id:
        return await bot.send_message(
            chat_id=chat_id,
            text=message,
            message_thread_id=thread_id,
            disable_web_page_preview=True,
            reply_to_message_id=reply_to_message_id,
        )
    else:
        return await bot.send_message(
            chat_id=chat_id,
            text=message,
            disable_web_page_preview=True,
            reply_to_message_id=reply_to_message_id,
        )
