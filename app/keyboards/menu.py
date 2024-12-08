from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def menu_keyboard_ru() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Добавить место 🏠', callback_data='add_place')
            ],
            [
                InlineKeyboardButton(text='Посмотреть места 👀', callback_data='show_places')
            ]
        ]
    )


def menu_keyboard_en() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Add a place 🏠', callback_data='add_place')
            ],
            [
                InlineKeyboardButton(text='Look at places 👀', callback_data='show_places')
            ]
        ]
    )