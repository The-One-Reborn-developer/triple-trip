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


admin_router = Router()


@admin_router.message(Command('admin'))
async def admin_panel_handler(message: Message):
    admin_check = get_user_producer(message.from_user.id)

    if not admin_check:
        pass
    else:
        await message.answer(
            admin_panel(),
            reply_markup=admin_keyboard()
        )


@admin_router.callback_query(F.data == 'location_monitoring')
async def monitor_locations_handler(callback: CallbackQuery):
    unvalidated_locations = get_unvalidated_locations_producer()

    if not unvalidated_locations:
        await callback.answer('Нет не проверенных локаций', show_alert=True)
    else:
        for location in unvalidated_locations:
            location_details = f'⏫\nНазвание: {location["name"]}\n' \
                               f'Страна: {location["country"]}\n' \
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