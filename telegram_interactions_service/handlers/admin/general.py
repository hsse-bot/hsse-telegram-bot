from aiogram import F, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router

from telegram_interactions_service.middlewares.admin_middleware import IsAdminMiddleware
from telegram_interactions_service.keyboards.inline import admin

admin_general_router = Router()


@admin_general_router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer("Админ панель", reply_markup=admin.admin_main_kb)


@admin_general_router.callback_query(admin.AdminMainMenuKb.filter(F.action == "/"))
async def call_admin_menu(callback: CallbackQuery):
    await callback.message.edit_text("Админ панель", reply_markup=admin.admin_main_kb)


@admin_general_router.callback_query(admin.AdminMainMenuKb.filter(F.action == "/material_help"))
async def call_material_help_menu(callback: CallbackQuery):
    await callback.message.edit_text("Меню сервиса матпомощи", reply_markup=admin.admin_material_help_menu_kb)


@admin_general_router.callback_query(admin.AdminMainMenuKb.filter(F.action == "/notify_service"))
async def call_notify_service_menu(callback: CallbackQuery):
    await callback.message.edit_text("Меню сервиса уведомлений", reply_markup=admin.admin_notify_service_menu_kb)


def setup(*, dispatcher: Dispatcher):
    admin_general_router.message.middleware(IsAdminMiddleware())
    dispatcher.include_router(admin_general_router)
