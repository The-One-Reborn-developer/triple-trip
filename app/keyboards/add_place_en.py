from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def one_more_photo_keyboard_en() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='One more photo 📸', callback_data='add_photo_en')
            ],
            [
                InlineKeyboardButton(text='Done ✅', callback_data='add_photo_done_en')
            ]
        ]
    )