from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.show_place_choose_country_en import choose_country_keyboard

from app.views.choose_country_en import choose_country


show_place_choose_country_en_router = Router()


@show_place_choose_country_en_router.callback_query(F.data)
async def test(callback: CallbackQuery):
    await callback.answer(callback.data, show_alert=True)


@show_place_choose_country_en_router.callback_query(F.data == 'show_places_en')
async def choose_country_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        choose_country(),
        reply_markup=choose_country_keyboard(1)
    )


@show_place_choose_country_en_router.callback_query(F.data.startswith('show_place_previous_page_en_'))
async def pagination_previous_handler(callback: CallbackQuery):
    page = int(callback.data.split('_')[-1])

    await callback.message.edit_reply_markup(
        reply_markup=choose_country_keyboard(page)
    )

    await callback.answer()


@show_place_choose_country_en_router.callback_query(F.data.startswith('show_place_next_page_en_'))
async def pagination_next_handler(callback: CallbackQuery):
    page = int(callback.data.split('_')[-1])

    await callback.message.edit_reply_markup(
        reply_markup=choose_country_keyboard(page)
    )

    await callback.answer()