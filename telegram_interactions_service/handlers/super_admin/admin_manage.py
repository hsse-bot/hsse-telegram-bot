import logging

from aiogram import Router, F, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from telegram_interactions_service.config import SUPER_ADMIN_TG_ID
from telegram_interactions_service.keyboards.inline import super_admin
from telegram_interactions_service.middlewares import IsSuperAdminMiddleware
from telegram_interactions_service.misc import dataclasses, message_templates, constants
from telegram_interactions_service.misc.constants import SUPER_ADMIN_MENU_COMMAND
from telegram_interactions_service.states.add_admin_states import AddAdminForm
from telegram_interactions_service.services_interactions.user_managing_service import UserManagingServiceInteraction


super_admin_manage_router = Router()
logger = logging.getLogger(__name__)


@super_admin_manage_router.message(Command(SUPER_ADMIN_MENU_COMMAND))
async def super_admin_menu_cmd(message: Message, state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()
    await message.answer("Меню супер админа:", reply_markup=super_admin.super_admin_main_kb())


@super_admin_manage_router.callback_query(super_admin.SuperAdminMainMenuKb.filter(F.action == "/"))
async def call_super_admin_menu(callback: CallbackQuery, state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()
    await callback.message.edit_text("Меню супер админа", reply_markup=super_admin.super_admin_main_kb())


@super_admin_manage_router.callback_query(super_admin.SuperAdminMainMenuKb.filter(F.action == "/admins"))
async def call_admins(callback: CallbackQuery):
    try:
        admins = await UserManagingServiceInteraction().get_admins()
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await callback.message.edit_text(message_templates.error_admin_text,
                                         reply_markup=super_admin.super_admin_main_kb())
        return
    if len(admins) == 0:
        await callback.message.edit_text(f"Пока что нет админов",
                                         reply_markup=super_admin.super_return_menu_kb())
        await callback.answer()
        return
    max_page = (len(admins) - 1) // constants.MAX_ADMINS_PER_PAGE
    await callback.message.edit_text(f"Админы: {1}/{max_page + 1}",
                                     reply_markup=super_admin.super_admins_paginator(admins, page=0))


@super_admin_manage_router.callback_query(super_admin.AdminsKb.filter(F.action.startswith("/id/")))
async def call_admin_handler(callback: CallbackQuery, callback_data: super_admin.AdminsKb):
    admin_id = int(callback_data.action[4:])
    await callback.message.edit_text(f"Админ с id {admin_id}",
                                     reply_markup=super_admin.super_admin_edit_kb(admin_id, callback_data.page))
    await callback.answer()


@super_admin_manage_router.callback_query(super_admin.AdminsKb.filter(F.action == "/"))
async def call_admins_handler(callback: CallbackQuery, callback_data: super_admin.AdminsKb):
    try:
        admins = await UserManagingServiceInteraction().get_admins()
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await callback.message.edit_text(message_templates.error_admin_text,
                                         reply_markup=super_admin.super_admin_main_kb())
        await callback.answer()
        return
    if len(admins) == 0:
        await callback.message.edit_text(f"Пока что нет админов",
                                         reply_markup=super_admin.super_return_menu_kb())
        await callback.answer()
        return
    max_page, cur_page = (len(admins) - 1) // constants.MAX_ADMINS_PER_PAGE, int(callback_data.page)
    await callback.message.edit_text(text=f"Админы: {cur_page + 1}/{max_page + 1}",
                                     reply_markup=super_admin.super_admins_paginator(admins, callback_data.page))
    await callback.answer()


@super_admin_manage_router.callback_query(super_admin.AdminsKb.filter(F.action.in_(["/prev", "/next"])))
async def call_admins_pagination_handler(callback: CallbackQuery, callback_data: super_admin.AdminsKb):
    try:
        admins = await UserManagingServiceInteraction().get_admins()
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await callback.message.edit_text(message_templates.error_admin_text,
                                         reply_markup=super_admin.super_admin_main_kb())
        await callback.answer()
        return
    if len(admins) == 0:
        await callback.message.edit_text(f"Пока что нет админов",
                                         reply_markup=super_admin.super_return_menu_kb())
        await callback.answer()
        return
    max_page, cur_page = (len(admins) - 1) // constants.MAX_ADMINS_PER_PAGE, int(callback_data.page)
    next_admins_page = cur_page
    if callback_data.action == "/next":
        if cur_page == max_page:
            await callback.answer()
            return
        next_admins_page = cur_page + 1 if cur_page < max_page else cur_page
    elif callback_data.action == "/prev":
        if cur_page == 0:
            await callback.message.edit_text("Меню супер админа",
                                             reply_markup=super_admin.super_admin_main_kb())
            await callback.answer()
            return
        next_admins_page = cur_page - 1
    await callback.message.edit_text(text=f"Админы: {next_admins_page + 1}/{max_page + 1}",
                                     reply_markup=super_admin.super_admins_paginator(admins, next_admins_page))
    await callback.answer()


@super_admin_manage_router.callback_query(super_admin.SuperAdminMainMenuKb.filter(F.action == "/create_admin"))
async def call_create_admin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddAdminForm.tg_id)
    await callback.message.answer("Введите его телеграмм айди:",
                                  reply_markup=super_admin.super_admin_cancel_to_main_menu_kb())
    await callback.message.delete()
    await callback.answer()


@super_admin_manage_router.message(AddAdminForm.tg_id)
async def receive_admin_tg_id(message: Message):
    if len(message.text.split()) != 1 or not message.text.isdigit():
        await message.answer("Неправильно указан id нового админа", reply_markup=super_admin.super_return_menu_kb())
        return
    try:
        new_admin = dataclasses.Admin(tg_id=int(message.text))
        if new_admin.tg_id == SUPER_ADMIN_TG_ID:
            await message.answer("Вы не можете сделать себя админом, вы супер админ",
                                 reply_markup=super_admin.super_return_menu_kb())
            return
        user_managing_service = UserManagingServiceInteraction()
        await user_managing_service.set_user_admin_role(new_admin.tg_id)
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await message.answer(message_templates.error_admin_text, reply_markup=super_admin.super_admin_main_kb())
        return
    await message.answer("Вы успешно добавили админа!", reply_markup=super_admin.super_return_menu_kb())


def setup(*, dispatcher: Dispatcher):
    super_admin_manage_router.message.middleware(IsSuperAdminMiddleware())
    dispatcher.include_router(super_admin_manage_router)
