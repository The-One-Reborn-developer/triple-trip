def no_locations() -> str:
    return 'There are no locations in this country yet 😔'


def location_details(name, address) -> str:
    return f'⏫\nName: {name}\n' \
           f'Address: {address}\n'