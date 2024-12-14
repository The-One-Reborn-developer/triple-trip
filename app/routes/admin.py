from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboards.admin import admin_keyboard

from app.views.admin import admin_panel


admin_router = Router()


@admin_router.message(Command('admin'))
async def admin_panel_handler(message: Message):
    await message.answer(
        admin_panel(),
        reply_markup=admin_keyboard()
    )