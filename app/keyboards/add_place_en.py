from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def add_place_photo_keyboard_en() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Done ✅', callback_data='add_photo_done_en')
            ]
        ]
    )