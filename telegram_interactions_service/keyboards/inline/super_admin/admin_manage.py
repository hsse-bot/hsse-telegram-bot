from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from typing import List
from telegram_interactions_service.misc import dataclasses, constants


class SuperAdminMainMenuKb(CallbackData, prefix="super_admin_menu"):
    action: str


class AdminsKb(CallbackData, prefix=SuperAdminMainMenuKb.__prefix__ + '/admins'):
    action: str
    page: int


class AdminEditKb(CallbackData, prefix=AdminsKb.__prefix__ + "/id"):
    action: str
    tg_id: int


def super_admin_main_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Админы", callback_data=SuperAdminMainMenuKb(action="/admins").pack())
    )
    builder.row(
        InlineKeyboardButton(text="Создать админа", callback_data=SuperAdminMainMenuKb(action="/create_admin").pack())
    )
    return builder.as_markup()


def super_admins_paginator(admins: List[dataclasses.Admin], page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    cur_index = page * constants.MAX_ADMINS_PER_PAGE
    for i in range(cur_index, min(len(admins), cur_index + constants.MAX_CATEGORIES_PER_PAGE)):
        builder.row(
            InlineKeyboardButton(text=f"Админ {admins[i].tg_id}",
                                 callback_data=AdminsKb(action=f"/id/{admins[i].tg_id}", page=page).pack()),
            width=1
        )
    builder.row(
        InlineKeyboardButton(text="⬅", callback_data=AdminsKb(action="/prev", page=page).pack()),
        InlineKeyboardButton(text="➡", callback_data=AdminsKb(action="/next", page=page).pack()),
        width=2
    )
    return builder.as_markup()


def super_admin_edit_kb(admin_tg_id: int, page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Удалить админа",
                             callback_data=AdminEditKb(action=f"/{admin_tg_id}/delete",
                                                       tg_id=admin_tg_id).pack()),
        width=1
    )
    builder.row(
        InlineKeyboardButton(text="⬅", callback_data=AdminsKb(action="/", page=page).pack()),
        width=1
    )
    return builder.as_markup()


def super_return_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅", callback_data=SuperAdminMainMenuKb(action="/").pack()),
        width=1
    )
    return builder.as_markup()
