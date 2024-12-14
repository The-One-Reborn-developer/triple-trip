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