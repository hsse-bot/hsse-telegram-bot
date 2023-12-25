from aiogram import F, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router

from telegram_interactions_service.keyboards.inline import user
from telegram_interactions_service.keyboards import reply
from telegram_interactions_service.middlewares import IsRegisteredMiddleware
from telegram_interactions_service.misc import constants, message_templates
from telegram_interactions_service.services_interactions.user_managing_service import UserManagingServiceInteraction
from telegram_interactions_service.config import SUPER_ADMIN_TG_ID


user_general_router = Router()


@user_general_router.message(Command("help"))
async def cmd_help(message: Message):
    user_role = (await UserManagingServiceInteraction().get_user(message.from_user.id)).role
    if message.from_user.id == SUPER_ADMIN_TG_ID:
        await message.answer('Какая тебе помощь, супер админ, ты тут главный! Тебе только Бог поможет',
                             reply_markup=reply.super_admin_reply_kb())
    elif user_role.name == constants.USER_ROLE_NAME:
        await message.answer(message_templates.help_message, reply_markup=reply.user_menu_reply_kb())
    elif user_role.name == constants.ADMIN_ROLE_NAME:
        await message.answer(message_templates.help_message, reply_markup=reply.admin_menu_reply_kb())


@user_general_router.message(Command(constants.USER_MENU_COMMAND))
async def cmd_menu(message: Message):
    await message.answer("Меню", reply_markup=user.user_main_kb())


@user_general_router.callback_query(user.UserMainMenuKb.filter(F.action == "/"))
async def call_admin_menu(callback: CallbackQuery):
    await callback.message.edit_text("Меню", reply_markup=user.user_main_kb())


@user_general_router.callback_query(user.UserMainMenuKb.filter(F.action == "/notify_service"))
async def call_notify_service_menu(callback: CallbackQuery):
    await callback.message.edit_text("Меню уведомлений", reply_markup=user.user_notify_service_menu_kb())


# @user_general_router.callback_query(user.UserMainMenuKb.filter(F.action == "/material_help"))
# async def call_material_help_menu(callback: CallbackQuery):
#     await callback.message.edit_text("Меню матпомощи", reply_markup=user.user_material_help_menu_kb)


def setup(*, dispatcher: Dispatcher):
    user_general_router.message.middleware(IsRegisteredMiddleware())
    dispatcher.include_router(user_general_router)
