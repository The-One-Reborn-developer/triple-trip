from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.keyboards.add_place_en import (
    add_place_photo_keyboard_en
)

from app.keyboards.menu_en import (
    menu_keyboard_en
)

from app.views.add_place_en import (
    place_name_en,
    place_address_en,
    place_photo_en,
    place_one_more_photo_en,
    place_added_en
)

from app.views.errors_en import (
    place_photo_error_en
)


add_place_en_router = Router()


class AddPlaceEn(StatesGroup):
    country_en = State()
    name_en = State()
    address_en = State()
    photos_en = State()


@add_place_en_router.callback_query(F.data == 'add_place_en')
async def add_place(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddPlaceEn.name_en)
    
    await callback.message.edit_text(
        place_name_en()
    )


@add_place_en_router.message(AddPlaceEn.name_en)
async def add_place_name_en(message: Message, state: FSMContext):
    await state.update_data(name_en=message.text)
    await state.set_state(AddPlaceEn.address_en)

    await message.answer(
        place_address_en()
    )


@add_place_en_router.message(AddPlaceEn.address_en)
async def add_place_address_en(message: Message, state: FSMContext):
    await state.update_data(address_en=message.text)
    await state.set_state(AddPlaceEn.photos_en)

    await message.answer(
        place_photo_en()
    )


@add_place_en_router.message(AddPlaceEn.photos_en)
async def add_place_first_photo_ru(message: Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get('photos_ru', [])

    if not message.photo:
        photos_amount = len(photos)

        if photos_amount == 0:
            await message.answer(
                place_photo_error_en()
            )
        elif photos_amount == 10:
            # TODO: add place to database for validation

            await state.clear()

            await message.answer(
                place_added_en(),
                reply_markup=menu_keyboard_en()
            )
    else:
        photo_id = message.photo[-1].file_id
        photos.append(photo_id)
        await state.update_data(photos_ru=photos)

        await message.answer(
            place_one_more_photo_en(),
            reply_markup=add_place_photo_keyboard_en()
        )


@add_place_en_router.callback_query(F.data == 'add_photo_done_en')
async def add_photo_done(callback: CallbackQuery, state: FSMContext):
    # TODO: add place to database for validation

    await state.clear()

    await callback.message.edit_text(
        place_added_en(),
        reply_markup=menu_keyboard_en()
    )