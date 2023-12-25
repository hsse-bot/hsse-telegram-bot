from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from typing import List
from telegram_interactions_service.misc import dataclasses, constants
from .admin_manage import SuperAdminMainMenuKb


class UsersKb(CallbackData, prefix=SuperAdminMainMenuKb.__prefix__ + '/users'):
    action: str


def super_user_manage_cancel_action() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Отмена", callback_data=SuperAdminMainMenuKb(action="/users").pack())
    )
    return builder.as_markup()


def super_user_return_user_manage_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Назад", callback_data=SuperAdminMainMenuKb(action="/users").pack())
    )
    return builder.as_markup()


def super_user_manage_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Список", callback_data=UsersKb(action="/get_users").pack()),
        InlineKeyboardButton(text="Удалить", callback_data=UsersKb(action="/delete_user").pack()),
        width=2
    )
    builder.row(
        InlineKeyboardButton(text="Забанить", callback_data=UsersKb(action="/ban_user").pack()),
        InlineKeyboardButton(text="Разбанить", callback_data=UsersKb(action="/unban_user").pack()),
        width=2
    )
    builder.row(
        InlineKeyboardButton(text="Назад", callback_data=SuperAdminMainMenuKb(action="/").pack())
    )
    return builder.as_markup()
