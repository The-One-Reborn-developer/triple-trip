from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def choose_option_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='В меню 🔙', callback_data='ru')
            ],
            [
                InlineKeyboardButton(text='Выбрать другую страну 👀', callback_data='show_places_ru')
            ]
        ]
    )