from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='English 🇬🇧', callback_data='english')
            ],
            [
                InlineKeyboardButton(text='Русский 🇷🇺', callback_data='russian')
            ]
        ]
    )