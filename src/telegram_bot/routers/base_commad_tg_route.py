from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from src.core.logger import logger
router = Router(name=__name__)


@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext) -> None:
    """
    Определяем обработчик для команды "/start".
    """

    current_state = await state.get_state()
    if current_state:
        await state.clear()

    await message.answer(
        text=(
            f"Здравствуйте, {message.from_user.full_name}! Ваш telegram_id: {message.from_user.id}."
            "Я буду информировать о важных действиях в вашем репозитории Git Lab."
        ),
        reply_markup=ReplyKeyboardRemove(),
    )
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Error deleting message: {e}")