def admin_panel() -> str:
    return 'Выберите опцию ⏬'


def location_details(name, country, address) -> str:
    return f'⏫\nНазвание: {name}\n' \
           f'Страна: {country}\n' \
           f'Адрес: {address}\n'


def no_unvalidated_locations() -> str:
    return 'Нет не проверенных локаций 🤷‍♂️'


def location_verified() -> str:
    return 'Локация одобрена ✅'


def location_declined() -> str:
    return 'Локация отклонена ❌'