from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Добавить место 🏠', callback_data='add_place_ru')
            ],
            [
                InlineKeyboardButton(text='Посмотреть места 👀', callback_data='show_places_ru')
            ]
        ]
    )