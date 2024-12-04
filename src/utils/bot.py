from src.telegram_bot.bot_main import bot
from aiogram.types import ReactionTypeEmoji


async def send_telegram_message(
    chat_id: int, message: str, thread_id: int = None, reply_to_message_id: int = None
):
    """Асинхронная функция для отправки сообщения через Telegram бота."""
    if thread_id != 0:
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


async def send_message_reaction(
    chat_id: int,
    message: str,
    reaction: str,
):
    """Асинхронная функция для установки реакции на сообщение."""

    return await bot.set_message_reaction(
        chat_id=chat_id,
        message_id=message,
        reaction=[ReactionTypeEmoji(emoji=reaction)],
    )
