import orjson

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def choose_country_keyboard(page) -> InlineKeyboardMarkup:
    data = orjson.loads(open('app/temp/countries_ru.json', 'rb').read())
    items_per_page = 20
    total_pages = (len(data) + items_per_page - 1) // items_per_page

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    page_data = data[start_index:end_index]

    keyboard = [
        [InlineKeyboardButton(text=country["name"], callback_data=f"add_place_country_ru_{country['code']}")]
        for country in page_data
    ]

    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(
            InlineKeyboardButton(text="⬅️ Назад", callback_data=f"add_place_previous_page_ru_{page - 1}")
        )
    if page < total_pages:
        pagination_buttons.append(
            InlineKeyboardButton(text="Вперед ➡️", callback_data=f"add_place_next_page_ru_{page + 1}")
        )

    if pagination_buttons:
        keyboard.append(pagination_buttons)

    back_to_menu_button = [
        InlineKeyboardButton(text="В меню 🔙", callback_data="ru")
    ]

    keyboard.append(back_to_menu_button)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)