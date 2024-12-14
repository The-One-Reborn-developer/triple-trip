from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.keyboards.admin import admin_keyboard

from app.views.admin import admin_panel

from app.tasks.get_user_producer import get_user_producer
from app.tasks.get_unvalidated_locations_producer import get_unvalidated_locations_producer


admin_router = Router()


class adminStates(StatesGroup):
    monitor_locations = State()


@admin_router.message(Command('admin'))
async def admin_panel_handler(message: Message, state: FSMContext):
    admin_check = get_user_producer(message.from_user.id)

    if not admin_check:
        pass
    else:
        await state.set_state(adminStates.monitor_locations)
        
        await message.answer(
            admin_panel(),
            reply_markup=admin_keyboard()
        )


@admin_router.callback_query(adminStates.monitor_locations)
async def monitor_locations_handler(callback: Message):
    unvalidated_locations = get_unvalidated_locations_producer()

    await callback.message.answer(
        str(unvalidated_locations)
    )