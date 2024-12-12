import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.keyboards.add_place_en import (
    add_place_photo_keyboard
)

from app.keyboards.menu_en import (
    menu_keyboard
)

from app.views.add_place_en import (
    place_name,
    place_address,
    place_photo,
    place_one_more_photo,
    place_added
)

from app.views.errors_en import (
    place_photo_error
)

from app.tasks.post_location_producer import post_location_producer


add_place_en_router = Router()


class AddPlaceEn(StatesGroup):
    country = State()
    name = State()
    address = State()
    photos = State()


@add_place_en_router.callback_query(F.data.startswith('add_place_country_en_'))
async def add_place_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddPlaceEn.country)
    await state.update_data(country=callback.data.split('_')[-1])
    await state.set_state(AddPlaceEn.name)

    await callback.message.edit_text(
        place_name()
    )


@add_place_en_router.message(AddPlaceEn.name)
async def add_place_name_handler(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddPlaceEn.address)

    await message.answer(
        place_address()
    )


@add_place_en_router.message(AddPlaceEn.address)
async def add_place_address_handler(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(AddPlaceEn.photos)

    await message.answer(
        place_photo()
    )


@add_place_en_router.message(AddPlaceEn.photos)
async def add_place_photo_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get('photos', [])

    if not message.photo:
        photos_amount = len(photos)

        if photos_amount == 0:
            await message.answer(
                place_photo_error()
            )
        elif photos_amount == 10:
            location_data = {
                'country': data['country'],
                'name': data['name'],
                'address': data['address'],
                'photos': photos
            }

            try:
                post_location_producer(location_data)
            except Exception as e:
                await message.answer('Error adding location to our database. Please try again or contact support 🙏')
                logging.error(f'Error in add_place_photo_handler adding location {data["name"]} to the database: {e}')

            await state.clear()

            await message.answer(
                place_added(),
                reply_markup=menu_keyboard()
            )
    else:
        photo_id = message.photo[-1].file_id
        photos.append(photo_id)
        await state.update_data(photos=photos)

        await message.answer(
            place_one_more_photo(),
            reply_markup=add_place_photo_keyboard()
        )


@add_place_en_router.callback_query(F.data == 'add_photo_done_en')
async def add_place_done_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    location_data = {
        'country': data['country'],
        'name': data['name'],
        'address': data['address'],
        'photos': data['photos']
    }

    try:
        post_location_producer(location_data)
    except Exception as e:
        await callback.answer('Error adding location to our database. Please try again or contact support 🙏',
                              show_alert=True)
        logging.error(f'Error in add_place_done_handler adding location {data["name"]} to the database: {e}')

    await state.clear()

    await callback.message.edit_text(
        place_added(),
        reply_markup=menu_keyboard()
    )