import logging

from aiogram import Router
from aiogram.filters import CommandStart

from app.keyboards.start import start_keyboard

from app.views.start import choose_language

from app.tasks.post_user_producer import post_user_producer


start_router = Router()


@start_router.message(CommandStart())
async def start(message):
    try:
        post_user_producer(message.from_user.id)
    except Exception as e:
        logging.error(f'Error in start_router adding user to database: {e}')

    await message.answer(choose_language(), reply_markup=start_keyboard())