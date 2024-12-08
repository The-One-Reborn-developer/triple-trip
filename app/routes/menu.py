import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.menu import (
    menu_keyboard_en,
    menu_keyboard_ru
)

from app.views.menu import (
    choose_option_en,
    choose_option_ru
)

from app.tasks.update_user_producer import update_user_producer


menu_router = Router()


@menu_router.callback_query(F.data == 'en')
async def menu_en(callback: CallbackQuery):
    try:
        update_user_producer(
            callback.from_user.id,
            languange='en'
        )
    except Exception as e:
        logging.error(f'Error in menu_en updating user in database: {e}')

    await callback.message.edit_text(
        choose_option_en(),
        reply_markup=menu_keyboard_en()
    )


@menu_router.callback_query(F.data == 'ru')
async def menu_ru(callback: CallbackQuery):
    try:
        update_user_producer(
            callback.from_user.id,
            languange='ru'
        )
    except Exception as e:
        logging.error(f'Error in menu_ru updating user in database: {e}')

    await callback.message.edit_text(
        choose_option_ru(),
        reply_markup=menu_keyboard_ru()
    )