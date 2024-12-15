import logging
import orjson

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.keyboards.admin import (
    admin_keyboard,
    location_keyboard
)

from app.views.admin import admin_panel

from app.tasks.get_user_producer import get_user_producer
from app.tasks.get_unvalidated_locations_producer import get_unvalidated_locations_producer
from app.tasks.update_location_producer import update_location_producer
from app.tasks.delete_location_producer import delete_location_producer


admin_router = Router()


@admin_router.message(Command('admin'))
async def admin_panel_handler(message: Message):
    try:
        admin_check = get_user_producer(message.from_user.id)

        if not admin_check:
            pass
        else:
            await message.answer(
                admin_panel(),
                reply_markup=admin_keyboard()
            )
    except Exception as e:
        await message.answer('Произошла ошибка при проверке пользователя', show_alert=True)
        logging.error(f'Error in admin_panel_handler checking user {message.from_user.id}: {e}')


@admin_router.callback_query(F.data == 'location_monitoring')
async def monitor_locations_handler(callback: CallbackQuery):
    try:
        unvalidated_locations = get_unvalidated_locations_producer()

        if not unvalidated_locations or len(unvalidated_locations) == 0:
            await callback.answer('Нет не проверенных локаций', show_alert=True)
        else:
            russian_country_names = {}

            with open('app/temp/countries_ru.json', 'rb') as f:
                russian_country_names_load = orjson.loads(f.read())

                russian_country_names = {
                    item['code']: item['name'] for item in russian_country_names_load
                }
            for location in unvalidated_locations:                
                country = russian_country_names.get(location['country'], '')
                logging.info(f'Found unvalidated location: {location}')
                logging.info(f'Country: {russian_country_names[location['country']]}')

                location_details = f'⏫\nНазвание: {location["name"]}\n' \
                                f'Страна: {country}\n' \
                                f'Адрес: {location["address"]}\n'
                
                location_media_group = []
                for photo in location['photos']:
                    location_media_group.append(
                        {
                            'type': 'photo',
                            'media': photo
                        }
                    )

                keyboard = location_keyboard(location['id'])
                
                await callback.bot.send_media_group(
                    chat_id=callback.from_user.id,
                    media=location_media_group
                )
                await callback.bot.send_message(
                    chat_id=callback.from_user.id,
                    text=location_details,
                    reply_markup=keyboard
                )
    except Exception as e:
        await callback.answer('Произошла ошибка при проверке локации', show_alert=True)
        logging.error(f'Error in monitor_locations_handler getting unvalidated locations: {e}')


@admin_router.callback_query(F.data.startswith('admin_location_approve_'))
async def approve_location_handler(callback: CallbackQuery):
    location_id = int(callback.data.split('_')[-1])
    
    try:
        approve_location_result = update_location_producer(location_id, is_verified=1)

        if approve_location_result:
            await callback.answer('Локация одобрена', show_alert=True)
        else:
            await callback.answer('Произошла ошибка при одобрении локации', show_alert=True)

    except Exception as e:
        await callback.answer('Произошла ошибка при одобрении локации', show_alert=True)
        logging.error(f'Error in approve_location_handler approving location {location_id}: {e}')


@admin_router.callback_query(F.data.startswith('admin_location_decline_'))
async def decline_location_handler(callback: CallbackQuery):
    location_id = int(callback.data.split('_')[-1])
    
    try:
        decline_location_result = delete_location_producer(location_id)

        if decline_location_result:
            await callback.answer('Локация отклонена', show_alert=True)
        else:
            await callback.answer('Произошла ошибка при отклонении локации', show_alert=True)

    except Exception as e:
        await callback.answer('Произошла ошибка при отклонении локации', show_alert=True)
        logging.error(f'Error in decline_location_handler declining location {location_id}: {e}')