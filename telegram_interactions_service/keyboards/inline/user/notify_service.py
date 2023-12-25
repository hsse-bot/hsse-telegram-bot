from typing import List

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_interactions_service.misc import constants, dataclasses
from telegram_interactions_service.keyboards.inline.user.main_menu import UserMainMenuKb


class NotifyServiceMenuKb(CallbackData, prefix=UserMainMenuKb.__prefix__ + "/notify_service"):
    action: str


class NotifyCategoriesKb(CallbackData, prefix=NotifyServiceMenuKb.__prefix__ + "/categories"):
    action: str
    page: int


def notify_categories_paginator_kb(all_categories: List[dataclasses.NotifyCategory],
                                   user_categories: List[dataclasses.NotifyCategory],
                                   page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    cur_index = page * constants.MAX_CATEGORIES_PER_PAGE
    for i in range(cur_index, min(len(all_categories), cur_index + constants.MAX_CATEGORIES_PER_PAGE)):
        if all_categories[i] in user_categories:
            builder.row(
                InlineKeyboardButton(
                    text=f"✅ {all_categories[i].name}",
                    callback_data=NotifyCategoriesKb(action=f"/id/unsub/{all_categories[i].id}",
                                                     page=page).pack()),
                width=1
            )
        else:
            builder.row(
                InlineKeyboardButton(
                    text=f"❌ {all_categories[i].name}",
                    callback_data=NotifyCategoriesKb(action=f"/id/sub/{all_categories[i].id}",
                                                     page=page).pack()),
                width=1
            )
    builder.row(
        InlineKeyboardButton(text="⬅", callback_data=NotifyCategoriesKb(action="/prev", page=page).pack()),
        InlineKeyboardButton(text="➡", callback_data=NotifyCategoriesKb(action="/next", page=page).pack()),
        width=2
    )
    return builder.as_markup()


def user_notify_service_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Мои подписки", callback_data=NotifyCategoriesKb(action="/", page=0).pack()),
        width=1
    )
    builder.row(
        InlineKeyboardButton(text="⬅", callback_data=UserMainMenuKb(action="/").pack()), width=1
    )
    return builder.as_markup()


def user_return_notify_categories_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔼", callback_data=NotifyCategoriesKb(action="/", page=0).pack()),
        width=1
    )
    return builder.as_markup()


def error_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅", callback_data=UserMainMenuKb(action="/").pack()),
        width=1
    )
    return builder.as_markup()
