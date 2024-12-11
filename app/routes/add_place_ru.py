from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.keyboards.add_place_ru import (
    add_place_photo_keyboard
)

from app.keyboards.menu_ru import (
    menu_keyboard
)

from app.views.add_place_ru import (
    place_name,
    place_address,
    place_photo,
    place_one_more_photo,
    place_added
)

from app.views.errors_ru import (
    place_photo_error
)


add_place_ru_router = Router()


class AddPlaceRu(StatesGroup):
    country = State()
    name = State()
    address = State()
    photos = State()


@add_place_ru_router.callback_query(F.data == 'add_place_ru')
async def add_place(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddPlaceRu.name)
    
    await callback.message.edit_text(
        place_name()
    )


@add_place_ru_router.message(AddPlaceRu.name)
async def add_place_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddPlaceRu.address)

    await message.answer(
        place_address()
    )


@add_place_ru_router.message(AddPlaceRu.address)
async def add_place_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(AddPlaceRu.photos)

    await message.answer(
        place_photo()
    )


@add_place_ru_router.message(AddPlaceRu.photos)
async def add_place_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get('photos', [])

    if not message.photo:
        photos_amount = len(photos)

        if photos_amount == 0:
            await message.answer(
                place_photo_error()
            )
        elif photos_amount == 10:
            # TODO: add place to database for validation

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


@add_place_ru_router.callback_query(F.data == 'add_photo_done_ru')
async def add_place_done(callback: CallbackQuery, state: FSMContext):
    # TODO: add place to database for validation

    await state.clear()

    await callback.message.edit_text(
        place_added(),
        reply_markup=menu_keyboard()
    )