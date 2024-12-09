import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.menu_ru import (
    menu_keyboard_ru
)

from app.views.menu_ru import (
    choose_option_ru
)

from app.tasks.update_user_producer import update_user_producer


menu_router_ru = Router()


@menu_router_ru.callback_query(F.data == 'ru')
async def menu_ru(callback: CallbackQuery):
    try:
        update_user_producer(
            callback.from_user.id,
            languange=callback.data
        )
    except Exception as e:
        logging.error(f'Error in menu_ru updating user in database: {e}')

    await callback.message.edit_text(
        choose_option_ru(),
        reply_markup=menu_keyboard_ru()
    )