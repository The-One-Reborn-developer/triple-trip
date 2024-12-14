from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Мониторинг локаций 🔍', callback_data='location_monitoring')
            ],
            [
                InlineKeyboardButton(text='Выйти из режима администратора 🚪', callback_data='ru')
            ]
        ]
    )


def location_keyboard(location_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Одобрить локацию ✅', callback_data=f'admin_location_approve_{location_id}')
            ],
            [
                InlineKeyboardButton(text='Отклонить локацию ❌', callback_data=f'admin_location_decline_{location_id}')
            ]
        ]
    )