import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.tasks.get_locations_by_country_producer import get_locations_by_country_producer


show_place_ru_router = Router()


@show_place_ru_router.callback_query(F.data.startswith('show_place_country_ru_'))
async def show_place_handler(callback: CallbackQuery):
    country_code = callback.data.split('_')[-1]

    try:
        locations = get_locations_by_country_producer(country_code)

        if locations:
            await callback.answer(str(locations))
    except Exception as e:
        await callback.answer('Произошла ошибка при получении локаций', show_alert=True)
        logging.error(f'Error in show_place_handler getting locations by country {country_code}: {e}')