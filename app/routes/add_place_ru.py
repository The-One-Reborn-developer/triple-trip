from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.keyboards.add_place_ru import (
    add_place_photo_keyboard_ru
)

from app.keyboards.menu_ru import (
    menu_keyboard_ru
)

from app.views.add_place_ru import (
    place_name_ru,
    place_address_ru,
    place_photo_ru,
    place_one_more_photo_ru,
    place_added_ru
)

from app.views.errors_ru import (
    place_photo_error_ru
)


add_place_ru_router = Router()


class AddPlaceRu(StatesGroup):
    name_ru = State()
    address_ru = State()
    photos_ru = State()


@add_place_ru_router.callback_query(F.data == 'add_place_ru')
async def add_place(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddPlaceRu.name_ru)
    
    await callback.message.edit_text(
        place_name_ru()
    )


@add_place_ru_router.message(AddPlaceRu.name_ru)
async def add_place_name_ru(message: Message, state: FSMContext):
    await state.update_data(name_ru=message.text)
    await state.set_state(AddPlaceRu.address_ru)

    await message.answer(
        place_address_ru()
    )


@add_place_ru_router.message(AddPlaceRu.address_ru)
async def add_place_address_ru(message: Message, state: FSMContext):
    await state.update_data(address_ru=message.text)
    await state.set_state(AddPlaceRu.photos_ru)

    await message.answer(
        place_photo_ru()
    )


@add_place_ru_router.message(AddPlaceRu.photos_ru)
async def add_place_first_photo_ru(message: Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get('photos_ru', [])

    if not message.photo:
        photos_amount = len(photos)

        if photos_amount == 0:
            await message.answer(
                place_photo_error_ru()
            )
        elif photos_amount == 10:
            # TODO: add place to database for validation

            await state.clear()

            await message.answer(
                place_added_ru(),
                reply_markup=menu_keyboard_ru()
            )
    else:
        photo_id = message.photo[-1].file_id
        photos.append(photo_id)
        await state.update_data(photos_ru=photos)

        await message.answer(
            f'{data}'
        )
        await message.answer(
            place_one_more_photo_ru(),
            reply_markup=add_place_photo_keyboard_ru()
        )


@add_place_ru_router.callback_query(F.data == 'add_photo_done_ru')
async def add_photo_done(callback: CallbackQuery, state: FSMContext):
    # TODO: add place to database for validation

    await state.clear()

    await callback.message.edit_text(
        place_added_ru(),
        reply_markup=menu_keyboard_ru()
    )