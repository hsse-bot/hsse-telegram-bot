from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class RegistrationKb(CallbackData, prefix="registration"):
    action: str


def cancel_registration_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Отменить", callback_data=RegistrationKb(action="/cancel").pack())
    )
    return builder.as_markup()


def confirm_registration_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅", callback_data=RegistrationKb(action="/confirm").pack()),
        InlineKeyboardButton(text="❌", callback_data=RegistrationKb(action="/cancel").pack()),
    )
    return builder.as_markup()
