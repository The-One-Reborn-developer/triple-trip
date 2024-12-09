from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def one_more_photo_ru() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Ещё фото 📸', callback_data='add_photo_ru')
            ],
            [
                InlineKeyboardButton(text='Готово ✅', callback_data='add_photo_done_ru')
            ]
        ]
    )