from typing import List

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_interactions_service.misc import constants, dataclasses
from telegram_interactions_service.keyboards.inline.user.main_menu import UserMainMenuKb


class ProfileMenuKb(CallbackData, prefix=UserMainMenuKb.__prefix__ + "/profile"):
    action: str


class ProfileChangeDataKb(CallbackData, prefix=ProfileMenuKb.__prefix__ + "/change"):
    action: str
    page: int


def profile_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Изменить данные", callback_data=ProfileChangeDataKb(action="/", page=0).pack()),
        width=1
    )
    builder.row(
        InlineKeyboardButton(text="⬅", callback_data=UserMainMenuKb(action="/").pack()), width=1
    )
    return builder.as_markup()


def profile_change_data_paginator_kb(page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    cur_index = page * constants.MAX_PROFILE_FIELD_PER_PAGE
    for i in range(cur_index, min(len(constants.all_student_info_fields), cur_index + constants.MAX_PROFILE_FIELD_PER_PAGE)):
        builder.row(
                InlineKeyboardButton(
                    text=f"{constants.all_student_info_fields[i].output_name}",
                    callback_data=ProfileChangeDataKb(action=f"/field/{constants.all_student_info_fields[i].db_name}",
                                                      page=page).pack()),
                width=1
            )
    builder.row(
        InlineKeyboardButton(text="⬅", callback_data=ProfileChangeDataKb(action="/prev", page=page).pack()),
        InlineKeyboardButton(text="➡", callback_data=ProfileChangeDataKb(action="/next", page=page).pack()),
        width=2
    )
    return builder.as_markup()


def cancel_data_changing_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Отменить", callback_data=UserMainMenuKb(action="/profile").pack())
    )
    return builder.as_markup()


def return_to_profile_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅", callback_data=UserMainMenuKb(action="/profile").pack())
    )
    return builder.as_markup()