from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from .main_menu import AdminMainMenuKb


class MaterialHelpMenuKb(CallbackData, prefix=AdminMainMenuKb.__prefix__ + "/material_help"):
    action: str


class MaterialHelpTicketsKb(CallbackData, prefix=MaterialHelpMenuKb.__prefix__ + "/tickets"):
    action: str
    page: int


def material_help_paginator(page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        *[InlineKeyboardButton(text=str(i + 1), callback_data=f"/ticket/{i + 1}") for i in
          range(page * 5, page * 5 + 5)],
        width=5
    )
    builder.row(
        InlineKeyboardButton(text="⬅", callback_data=MaterialHelpTicketsKb(action="/prev", page=page).pack()),
        InlineKeyboardButton(text="➡", callback_data=MaterialHelpTicketsKb(action="/next", page=page).pack()),
        width=2
    )
    return builder.as_markup()


def admin_material_help_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Заявки на матпомощь", callback_data=MaterialHelpMenuKb(action="/tickets").pack()),
        width=1
    )
    return builder.as_markup()
