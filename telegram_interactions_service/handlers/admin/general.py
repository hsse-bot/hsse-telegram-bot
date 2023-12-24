import logging

from aiogram import F, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router

from telegram_interactions_service.misc import message_templates
from telegram_interactions_service.middlewares import IsAdminMiddleware
from telegram_interactions_service.keyboards.inline import admin
from telegram_interactions_service.misc.constants import ADMIN_MENU_COMMAND
from telegram_interactions_service.services_interactions.user_managing_service import UserManagingServiceInteraction

admin_general_router = Router()
logger = logging.getLogger(__name__)


@admin_general_router.message(Command(ADMIN_MENU_COMMAND))
async def cmd_menu(message: Message):
    await message.answer("Админ панель", reply_markup=admin.admin_main_kb())


@admin_general_router.callback_query(admin.AdminMainMenuKb.filter(F.action == "/"))
async def call_admin_menu(callback: CallbackQuery):
    await callback.message.edit_text("Админ панель", reply_markup=admin.admin_main_kb())


@admin_general_router.callback_query(admin.AdminMainMenuKb.filter(F.action == "/material_help"))
async def call_material_help_menu(callback: CallbackQuery):
    await callback.message.edit_text("Меню сервиса матпомощи", reply_markup=admin.admin_material_help_menu_kb())


@admin_general_router.callback_query(admin.AdminMainMenuKb.filter(F.action == "/notify_service"))
async def call_notify_service_menu(callback: CallbackQuery):
    await callback.message.edit_text("Меню сервиса уведомлений", reply_markup=admin.admin_notify_service_menu_kb())


@admin_general_router.callback_query(admin.AdminMainMenuKb.filter(F.action == "/get_users"))
async def call_get_users(callback: CallbackQuery):
    try:
        all_users = await UserManagingServiceInteraction().get_all_users()
        result = '\n'.join([f"{user.name} {user.surname} {user.tg_id}" for user in all_users])
        await callback.message.edit_text(text="Имя Фамилия Telegram id\n" + result,
                                         reply_markup=admin.return_main_menu())
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await callback.message.edit_text(message_templates.error_admin_text,
                                         reply_markup=admin.admin_notify_service_menu_kb())
        await callback.answer()


def setup(*, dispatcher: Dispatcher):
    admin_general_router.message.middleware(IsAdminMiddleware())
    dispatcher.include_router(admin_general_router)
