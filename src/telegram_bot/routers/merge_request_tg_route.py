# TODO: доработать вебхук для взаимодействия с сообщениями и ботом

# from aiogram import Router, types
# from aiogram.fsm.context import FSMContext
# from aiogram.types import ReplyKeyboardRemove

# router = Router(name=__name__)


# @router.message()
# async def send_message(message: types.Message, state: FSMContext) -> None:
#     """
#     Отправляем сообщение в чат.
#     """

#     current_state = await state.get_state()
#     if current_state:
#         await state.clear()

#     await message.answer(
#         f"Здравствуйте, {message.from_user.full_name}! Ваш telegram_id: {message.from_user.id}.",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     await message.delete()
