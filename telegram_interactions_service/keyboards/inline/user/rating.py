from typing import List

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_interactions_service.misc import constants, dataclasses
from telegram_interactions_service.keyboards.inline.user.main_menu import UserMainMenuKb


class RatingMenuKb(CallbackData, prefix=UserMainMenuKb.__prefix__ + "/rating"):
    action: str


def rating_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅", callback_data=UserMainMenuKb(action="/").pack()), width=1
    )
    return builder.as_markup()