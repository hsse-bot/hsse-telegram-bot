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
    builder.row(
        InlineKeyboardButton(text="Пользователи", callback_data=AdminMainMenuKb(action="/get_users").pack())
    )
    return builder.as_markup()


def return_main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Назад", callback_data=AdminMainMenuKb(action="/").pack())
    )
    return builder.as_markup()
