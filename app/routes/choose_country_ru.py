from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.choose_country_ru import choose_country_keyboard

from app.views.choose_country_ru import choose_country


choose_country_ru_router = Router()


@choose_country_ru_router.callback_query(F.data == 'add_place_ru')
async def choose_country_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        choose_country(),
        reply_markup=choose_country_keyboard(1)
    )


@choose_country_ru_router.callback_query(F.data.startswith('previous_page_ru_') or F.data.startswith('next_page_ru_'))
async def pagination_handler(callback: CallbackQuery):
    page = int(callback.data.split('_')[-1])

    await callback.message.edit_reply_markup(
        reply_markup=choose_country_keyboard(page)
    )

    await callback.answer()