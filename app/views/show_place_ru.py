def no_locations() -> str:
    return 'В данной стране пока нет локаций 😔'


def location_details(name, address) -> str:
    return f'⏫\nНазвание: {name}\n' \
           f'Адрес: {address}\n'


def choose_option() -> str:
    return 'Выберите опцию ⏬'