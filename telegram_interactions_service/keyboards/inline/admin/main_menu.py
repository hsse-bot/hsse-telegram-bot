from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class AdminMainMenuKb(CallbackData, prefix="admin_menu"):
    action: str


admin_main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Заявки на матпомощь",
                                 callback_data=AdminMainMenuKb(action="/material_help").pack()),
            InlineKeyboardButton(text="Серсис уведомлений",
                                 callback_data=AdminMainMenuKb(action="/notify_service").pack())
        ]
    ]
)

admin_return_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="В меню 🔼", callback_data=AdminMainMenuKb(action="/").pack())
        ]
    ]
)
