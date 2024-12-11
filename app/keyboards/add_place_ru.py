from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def add_place_photo_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Готово ✅', callback_data='add_photo_done_ru')
            ]
        ]
    )