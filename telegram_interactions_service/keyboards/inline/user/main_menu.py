from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class UserMainMenuKb(CallbackData, prefix="user_menu"):
    action: str


def user_main_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Матпомощь",
                             callback_data=UserMainMenuKb(action="/material_help").pack()),
        InlineKeyboardButton(text="Уведомления",
                             callback_data=UserMainMenuKb(action="/notify_service").pack()),
        width=2
    )
    return builder.as_markup()
