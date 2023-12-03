from aiogram import F, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress

from telegram_interactions_service.middlewares.admin_middleware import IsAdminMiddleware
from telegram_interactions_service.keyboards.inline import admin

material_help_router = Router()


# @material_help_router.message(Command("material_help"))
# async def cmd_tickets(message: Message):
#     await message.answer("Меню сервиса матпомощи",
#                          reply_markup=inline_admin.admin_material_help_menu_kb)
#
#
# @material_help_router.callback_query(inline_admin.MaterialHelpMenuKbr.filter(F.action == "tickets"))
# async def call_tickets_pagination_handler(callback: CallbackQuery, callback_data: inline_admin.MaterialHelpMenuKbr):
#     page_number = int(callback_data.page)
#     next_page = page_number
#     if callback_data.action == "/next":
#         next_page = page_number + 1 if page_number < 5 else page_number
#     elif callback_data.action == "/prev":
#         next_page = page_number - 1 if page_number > 0 else page_number
#
#     with suppress(TelegramBadRequest):
#         await callback.message.edit_text(inline_admin.gen_ticket_pagination_page_text(next_page),
#                                          reply_markup=inline_admin.material_help_paginator(next_page))
#     await callback.answer()
#
#
# @material_help_router.callback_query(inline_admin.MaterialHelpMenuKbr.filter(F.action == "tickets!"))
# async def call_ticket_handler(callback: CallbackQuery, callback_data: inline_admin.MaterialHelpMenuKbr):
#     page_number = int(callback_data.page)
#     next_page = page_number
#     if callback_data.action == "/next":
#         next_page = page_number + 1 if page_number < 5 else page_number
#     elif callback_data.action == "/prev":
#         next_page = page_number - 1 if page_number > 0 else page_number
#
#     await callback.message.edit_text(inline_admin.gen_ticket_pagination_page_text(next_page),
#                                      reply_markup=inline_admin.material_help_paginator(next_page))
#     await callback.answer()


def setup(*, dispatcher: Dispatcher):
    material_help_router.message.middleware(IsAdminMiddleware())
    dispatcher.include_router(material_help_router)
