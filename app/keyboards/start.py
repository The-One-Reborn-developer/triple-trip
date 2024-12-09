from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='English 🇬🇧', callback_data='en')
            ],
            [
                InlineKeyboardButton(text='Русский 🇷🇺', callback_data='ru')
            ]
        ]
    )