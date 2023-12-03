from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class AdminMainMenuKb(CallbackData, prefix="admin_menu"):
    action: str


def admin_main_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        *[InlineKeyboardButton(text="Заявки на матпомощь",
                               callback_data=AdminMainMenuKb(action="/material_help").pack()),
          InlineKeyboardButton(text="Серсис уведомлений",
                               callback_data=AdminMainMenuKb(action="/notify_service").pack())],
        width=2
    )
    return builder.as_markup()
