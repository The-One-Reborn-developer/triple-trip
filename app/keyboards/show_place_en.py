from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def choose_option_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Back to menu 🔙', callback_data='en')
            ],
            [
                InlineKeyboardButton(text='Choose another country 👀', callback_data='show_places_en')
            ]
        ]
    )