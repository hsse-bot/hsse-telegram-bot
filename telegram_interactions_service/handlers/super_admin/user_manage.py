import logging

from aiogram import Router, F, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from telegram_interactions_service.config import SUPER_ADMIN_TG_ID
from telegram_interactions_service.keyboards.inline import super_admin
from telegram_interactions_service.middlewares import IsSuperAdminMiddleware
from telegram_interactions_service.misc import dataclasses, message_templates, constants
from telegram_interactions_service.states.super_user_manage_states import BanUserForm, DeleteUserForm, UnbanUserForm
from telegram_interactions_service.services_interactions.user_managing_service import UserManagingServiceInteraction

super_user_manage_router = Router()
logger = logging.getLogger(__name__)


@super_user_manage_router.callback_query(super_admin.SuperAdminMainMenuKb.filter(F.action == "/users"))
async def call_user_manage_manu(callback: CallbackQuery):
    await callback.message.edit_text(text="Меню управления пользователями",
                                     reply_markup=super_admin.super_user_manage_menu_kb())


@super_user_manage_router.callback_query(super_admin.UsersKb.filter(F.action == "/ban_user"))
async def call_ban_user(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BanUserForm.tg_id)
    await callback.message.edit_text(text="Введите телеграм id пользователя, которого вы хотите забанить",
                                     reply_markup=super_admin.super_user_manage_cancel_action())


@super_user_manage_router.message(BanUserForm.tg_id)
async def receive_ban_user_id(message: Message, state: FSMContext):
    user_id = message.text
    await state.clear()
    if not user_id.isdigit():
        await message.answer("Вы ввели не id!", reply_markup=super_admin.super_user_return_user_manage_menu_kb())
        return
    if int(user_id) == SUPER_ADMIN_TG_ID or int(user_id) == message.from_user.id:
        await message.answer("Вы не можете забанить такого пользователя!",
                             reply_markup=super_admin.super_user_return_user_manage_menu_kb())
        return
    try:
        await UserManagingServiceInteraction().ban_user(int(user_id))
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await message.answer(message_templates.error_admin_text,
                             reply_markup=super_admin.super_user_return_user_manage_menu_kb())
        return
    await message.answer("Вы успешно забанили пользователя!",
                         reply_markup=super_admin.super_user_return_user_manage_menu_kb())


@super_user_manage_router.callback_query(super_admin.UsersKb.filter(F.action == "/delete_user"))
async def call_delete_user(callback: CallbackQuery, state: FSMContext):
    await state.set_state(DeleteUserForm.tg_id)
    await callback.message.edit_text(text="Введите телеграм id пользователя, которого вы хотите удалить",
                                     reply_markup=super_admin.super_user_manage_cancel_action())


@super_user_manage_router.message(DeleteUserForm.tg_id)
async def receive_delete_user_id(message: Message, state: FSMContext):
    user_id = message.text
    await state.clear()
    if not user_id.isdigit():
        await message.answer("Вы ввели не id!", reply_markup=super_admin.super_user_return_user_manage_menu_kb())
        return
    if int(user_id) == SUPER_ADMIN_TG_ID or int(user_id) == message.from_user.id:
        await message.answer("Вы не можете удалить такого пользователя!",
                             reply_markup=super_admin.super_user_return_user_manage_menu_kb())
        return
    try:
        await UserManagingServiceInteraction().delete_user(int(user_id))
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await message.answer(message_templates.error_admin_text,
                             reply_markup=super_admin.super_user_return_user_manage_menu_kb())
        return
    await message.answer("Вы успешно удалили пользователя!",
                         reply_markup=super_admin.super_user_return_user_manage_menu_kb())


@super_user_manage_router.callback_query(super_admin.UsersKb.filter(F.action == "/unban_user"))
async def call_unban_user(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UnbanUserForm.tg_id)
    await callback.message.edit_text(text="Введите телеграм id пользователя, которого вы хотите разбанить",
                                     reply_markup=super_admin.super_user_manage_cancel_action())


@super_user_manage_router.message(UnbanUserForm.tg_id)
async def receive_unban_user_id(message: Message, state: FSMContext):
    user_id = message.text
    await state.clear()
    if not user_id.isdigit():
        await message.answer("Вы ввели не id!", reply_markup=super_admin.super_user_return_user_manage_menu_kb())
        return
    if int(user_id) == SUPER_ADMIN_TG_ID or int(user_id) == message.from_user.id:
        await message.answer("Вы не можете разбанить такого пользователя!",
                             reply_markup=super_admin.super_user_return_user_manage_menu_kb())
        return
    try:
        await UserManagingServiceInteraction().unban_user(int(user_id))
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await message.answer(message_templates.error_admin_text,
                             reply_markup=super_admin.super_user_return_user_manage_menu_kb())
        return
    await message.answer("Вы успешно разбанили пользователя!",
                         reply_markup=super_admin.super_user_return_user_manage_menu_kb())


def setup(*, dispatcher: Dispatcher):
    super_user_manage_router.message.middleware(IsSuperAdminMiddleware())
    dispatcher.include_router(super_user_manage_router)
