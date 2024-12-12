from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.add_place_choose_country_en import choose_country_keyboard

from app.views.choose_country_en import choose_country


add_place_choose_country_en_router = Router()


@add_place_choose_country_en_router.callback_query(F.data == 'add_place_en')
async def choose_country_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        choose_country(),
        reply_markup=choose_country_keyboard(1)
    )


@add_place_choose_country_en_router.callback_query(F.data.startswith('add_place_previous_page_en_'))
async def pagination_previous_handler(callback: CallbackQuery):
    page = int(callback.data.split('_')[-1])

    await callback.message.edit_reply_markup(
        reply_markup=choose_country_keyboard(page)
    )

    await callback.answer()


@add_place_choose_country_en_router.callback_query(F.data.startswith('add_place_next_page_en_'))
async def pagination_next_handler(callback: CallbackQuery):
    page = int(callback.data.split('_')[-1])

    await callback.message.edit_reply_markup(
        reply_markup=choose_country_keyboard(page)
    )

    await callback.answer()