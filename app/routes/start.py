import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from app.keyboards.start import start_keyboard

from app.views.start import choose_language
from app.views.errors_en import start_error

from app.tasks.post_user_producer import post_user_producer


start_router = Router()


@start_router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()

    try:
        post_user_producer(message.from_user.id)
    except Exception as e:
        await message.answer(start_error())
        logging.error(f'Error in start_router adding user to database: {e}')

    await message.answer(
        choose_language(),
        reply_markup=start_keyboard()
    )