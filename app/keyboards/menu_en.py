from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Add a place 🏠', callback_data='add_place_en')
            ],
            [
                InlineKeyboardButton(text='Look at places 👀', callback_data='show_places_en')
            ]
        ]
    )