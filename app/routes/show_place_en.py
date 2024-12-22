import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.views.errors_en import show_place_error

from app.tasks.get_locations_by_country_producer import get_locations_by_country_producer


show_place_en_router = Router()


@show_place_en_router.callback_query(F.data.startswith('show_place_country_en_'))
async def show_place_handler(callback: CallbackQuery):
    country_code = callback.data.split('_')[-1]
    await callback.message.delete()

    try:
        locations = get_locations_by_country_producer(country_code)

        if not locations:
            await callback.answer(show_place_error(), show_alert=True)
        else:
            for location in locations:
                location_details = f'⏫\nНазвание: {location["name"]}\n' \
                                f'Адрес: {location["address"]}\n'
                
                location_media_group = []
                for photo in location['photos']:
                    location_media_group.append(
                        {
                            'type': 'photo',
                            'media': photo
                        }
                    )
                
                await callback.bot.send_media_group(
                    chat_id=callback.from_user.id,
                    media=location_media_group
                )
                await callback.message.answer(
                    location_details
                )
    except Exception as e:
        await callback.answer(show_place_error(), show_alert=True)
        logging.error(f'Error in show_place_handler getting locations by country {country_code}: {e}')