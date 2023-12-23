from aiogram import F, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router

from telegram_interactions_service.middlewares import IsRegisteredMiddleware
from telegram_interactions_service.keyboards.inline import user

user_general_router = Router()


@user_general_router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer("Меню", reply_markup=user.user_main_kb())


@user_general_router.callback_query(user.UserMainMenuKb.filter(F.action == "/"))
async def call_admin_menu(callback: CallbackQuery):
    await callback.message.edit_text("Меню", reply_markup=user.user_main_kb())


# @user_general_router.callback_query(user.UserMainMenuKb.filter(F.action == "/material_help"))
# async def call_material_help_menu(callback: CallbackQuery):
#     await callback.message.edit_text("Меню матпомощи", reply_markup=user.user_material_help_menu_kb)


@user_general_router.callback_query(user.UserMainMenuKb.filter(F.action == "/notify_service"))
async def call_notify_service_menu(callback: CallbackQuery):
    await callback.message.edit_text("Меню уведомлений", reply_markup=user.user_notify_service_menu_kb())


def setup(*, dispatcher: Dispatcher):
    user_general_router.message.middleware(IsRegisteredMiddleware())
    dispatcher.include_router(user_general_router)
