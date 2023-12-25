from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from telegram_interactions_service.misc.constants import USER_MENU_COMMAND, ADMIN_MENU_COMMAND, SUPER_ADMIN_MENU_COMMAND


def user_menu_reply_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="/" + USER_MENU_COMMAND),
        width=1
    )
    return builder.as_markup(resize_keyboard=True)


def admin_menu_reply_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="/" + USER_MENU_COMMAND),
        width=1
    )
    builder.row(
        KeyboardButton(text="/" + ADMIN_MENU_COMMAND),
        width=1
    )
    return builder.as_markup()


def super_admin_reply_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="/" + USER_MENU_COMMAND),
        width=1
    )
    builder.row(
        KeyboardButton(text="/" + ADMIN_MENU_COMMAND),
        width=1
    )
    builder.row(
        KeyboardButton(text="/" + SUPER_ADMIN_MENU_COMMAND),
        width=1
    )
    return builder.as_markup()
