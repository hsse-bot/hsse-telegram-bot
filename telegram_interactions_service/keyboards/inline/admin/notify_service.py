from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from telegram_interactions_service.misc import constants, dataclasses
from .main_menu import AdminMainMenuKb
from typing import List


class NotifyServiceMenuKb(CallbackData, prefix=AdminMainMenuKb.__prefix__ + "/notify_service"):
    action: str


class NotifyCategoriesKb(CallbackData, prefix=NotifyServiceMenuKb.__prefix__ + "/categories"):
    action: str
    page: int


class NotifyCategoryKb(CallbackData, prefix=NotifyCategoriesKb.__prefix__ + "/id"):
    action: str
    category_id: int


def notify_categories_paginator(categories: List[dataclasses.NotifyCategory], page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    cur_index = page * constants.MAX_CATEGORIES_PER_PAGE
    for i in range(cur_index, min(len(categories), cur_index + constants.MAX_CATEGORIES_PER_PAGE)):
        builder.row(
            InlineKeyboardButton(text=f"{categories[i].name}",
                                 callback_data=NotifyCategoriesKb(action=f"/id/{categories[i].id}", page=page).pack()),
            width=1
        )
    builder.row(
        InlineKeyboardButton(text="⬅", callback_data=NotifyCategoriesKb(action="/prev", page=page).pack()),
        InlineKeyboardButton(text="➡", callback_data=NotifyCategoriesKb(action="/next", page=page).pack()),
        width=2
    )
    return builder.as_markup()


def admin_notify_category_kb(category_id: int, page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Отправить сообщение",
                             callback_data=NotifyCategoryKb(action=f"/{category_id}/send_text",
                                                            category_id=category_id).pack()),
        width=1
    )
    builder.row(
        InlineKeyboardButton(text="Удалить категорию",
                             callback_data=NotifyCategoryKb(action=f"/{category_id}/delete",
                                                            category_id=category_id).pack()),
        width=1
    )
    builder.row(
        InlineKeyboardButton(text="⬅", callback_data=NotifyCategoriesKb(action="/", page=page).pack()),
        width=1
    )
    return builder.as_markup()


def admin_notify_service_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Все категории", callback_data=NotifyCategoriesKb(action="/", page=0).pack()),
        width=1
    )
    builder.row(
        InlineKeyboardButton(text="Создать категорию",
                             callback_data=NotifyServiceMenuKb(action="/create_category").pack()),
        width=1
    )
    builder.row(InlineKeyboardButton(text="⬅", callback_data=AdminMainMenuKb(action="/").pack()), width=1)
    return builder.as_markup()


def admin_return_notify_categories_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔼", callback_data=NotifyCategoriesKb(action="/", page=0).pack()),
        width=1
    )
    return builder.as_markup()


def admin_return_notify_service_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔼", callback_data=NotifyServiceMenuKb(action="/").pack()),
        width=1
    )
    return builder.as_markup()
