import logging

from aiogram import F, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router

from telegram_interactions_service.states.notify_service_states import NotifySendTextForm, CreateCategoryForm
from telegram_interactions_service.misc import dataclasses, constants, message_templates
from telegram_interactions_service.middlewares.admin_middleware import IsAdminMiddleware
from telegram_interactions_service.keyboards.inline import admin
from telegram_interactions_service.services_interactions.telegram_notifier_service import \
    TelegramNotifierServiceInteraction

notify_service_router = Router()
logger = logging.getLogger(__name__)


@notify_service_router.message(Command("notify_service_admin"))
async def cmd_notify_service(message: Message, state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()
    await message.answer("Меню сервиса уведомлений", reply_markup=admin.admin_notify_service_menu_kb())


@notify_service_router.callback_query(admin.NotifyServiceMenuKb.filter(F.action == "/"))
async def call_notify_menu_handler(callback: CallbackQuery, callback_data: admin.NotifyCategoriesKb, state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()
    await callback.message.edit_text("Меню сервиса уведомлений", reply_markup=admin.admin_notify_service_menu_kb())
    await callback.answer()


@notify_service_router.callback_query(admin.NotifyCategoriesKb.filter(F.action == "/"))
async def call_categories_handler(callback: CallbackQuery, callback_data: admin.NotifyCategoriesKb,  state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()
    try:
        categories = await TelegramNotifierServiceInteraction().get_all_categories()
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await callback.message.edit_text(message_templates.error_admin_text,
                                         reply_markup=admin.admin_notify_service_menu_kb())
        await callback.answer()
        return
    if len(categories) == 0:
        await callback.message.edit_text(f"Пока что нет категорий уведомлений",
                                         reply_markup=admin.admin_return_notify_service_menu_kb())
        await callback.answer()
        return
    max_page, cur_page = (len(categories) - 1) // constants.MAX_CATEGORIES_PER_PAGE, int(callback_data.page)
    await callback.message.edit_text(f"Категории уведомлений: {cur_page+1}/{max_page+1}",
                                     reply_markup=admin.notify_categories_paginator(categories, callback_data.page))
    await callback.answer()


@notify_service_router.callback_query(admin.NotifyCategoriesKb.filter(F.action.in_(["/prev", "/next"])))
async def call_categories_pagination_handler(callback: CallbackQuery, callback_data: admin.NotifyCategoriesKb):
    try:
        categories = await TelegramNotifierServiceInteraction().get_all_categories()
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await callback.message.edit_text(message_templates.error_admin_text,
                                         reply_markup=admin.admin_notify_service_menu_kb())
        await callback.answer()
        return
    if len(categories) == 0:
        await callback.message.edit_text(f"Пока что нет категорий уведомлений",
                                         reply_markup=admin.admin_return_notify_service_menu_kb())
        await callback.answer()
        return
    max_page, cur_page = (len(categories) - 1) // constants.MAX_CATEGORIES_PER_PAGE, int(callback_data.page)
    next_categories_page = cur_page
    if callback_data.action == "/next":
        if cur_page == max_page:
            await callback.answer()
            return
        next_categories_page = cur_page + 1 if cur_page < max_page else cur_page
    elif callback_data.action == "/prev":
        if cur_page == 0:
            await callback.message.edit_text("Меню сервиса уведомлений",
                                             reply_markup=admin.admin_notify_service_menu_kb())
            await callback.answer()
            return
        next_categories_page = cur_page - 1
    await callback.message.edit_text(text=f"Категории уведомлений: {next_categories_page+1}/{max_page+1}",
                                     reply_markup=admin.notify_categories_paginator(categories, next_categories_page))
    await callback.answer()


@notify_service_router.callback_query(admin.NotifyCategoriesKb.filter(F.action.startswith("/id/")))
async def call_category_handler(callback: CallbackQuery, callback_data: admin.NotifyCategoriesKb):
    try:
        category_id = int(callback_data.action[4:])
        category = await TelegramNotifierServiceInteraction().get_category(category_id)
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await callback.message.edit_text(message_templates.error_admin_text,
                                         reply_markup=admin.admin_return_notify_service_menu_kb())
        await callback.answer()
        return
    await callback.message.edit_text(f"Категория {category.name}",
                                     reply_markup=admin.admin_notify_category_kb(category_id, callback_data.page))
    await callback.answer()


@notify_service_router.callback_query(admin.NotifyCategoryKb.filter(F.action.endswith("/send_text")))
async def call_send_text_handler(callback: CallbackQuery, callback_data: admin.NotifyCategoryKb, state: FSMContext):
    category_id = callback_data.category_id
    await state.set_state(NotifySendTextForm.text)
    await state.update_data(category_id=category_id)
    await callback.message.edit_text("Введите текст сообщения:", reply_markup=admin.admin_cancel_sending_message_category())
    await callback.answer()


@notify_service_router.message(NotifySendTextForm.text)
async def receive_notify_message_text(message: Message, state: FSMContext):
    category_id = (await state.get_data())["category_id"]
    try:
        category = await TelegramNotifierServiceInteraction().get_category(category_id)
        await TelegramNotifierServiceInteraction().notify(category_id, f"📢 {category.name}\n" + message.text)
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await message.answer(message_templates.error_admin_text, reply_markup=admin.admin_notify_service_menu_kb())
        return
    await state.clear()
    await message.answer(f"Вы успешно отправили текст {message.text}",
                         reply_markup=admin.admin_return_notify_categories_kb())


@notify_service_router.callback_query(admin.NotifyCategoryKb.filter(F.action.endswith("/delete")))
async def call_delete_category_handler(callback: CallbackQuery, callback_data: admin.NotifyCategoryKb):
    category_id = callback_data.category_id
    try:
        category = await TelegramNotifierServiceInteraction().get_category(category_id)
        await TelegramNotifierServiceInteraction().delete_category(category_id)
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await callback.message.edit_text(message_templates.error_admin_text,
                                         reply_markup=admin.admin_notify_service_menu_kb())
        await callback.answer()
        return
    await callback.message.edit_text(f"Вы успешно удалили категорию {category.name}",
                                     reply_markup=admin.admin_return_notify_categories_kb())
    await callback.answer()


@notify_service_router.callback_query(admin.NotifyServiceMenuKb.filter(F.action == "/create_category"))
async def call_create_category(callback: CallbackQuery, callback_data: admin.NotifyServiceMenuKb, state: FSMContext):
    await state.set_state(CreateCategoryForm.name)
    await callback.message.edit_text("Введите название новой категории:", reply_markup=admin.admin_cancel_creating_category())
    await callback.answer()


@notify_service_router.message(CreateCategoryForm.name)
async def receive_created_category_name(message: Message, state: FSMContext):
    await state.clear()
    try:
        await TelegramNotifierServiceInteraction().create_category(message.text)
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await message.answer(message_templates.error_admin_text, reply_markup=admin.admin_notify_service_menu_kb())
        return
    await message.answer(f"Вы успешно создали категорию {message.text}",
                         reply_markup=admin.admin_return_notify_service_menu_kb())


def setup(*, dispatcher: Dispatcher):
    notify_service_router.message.middleware(IsAdminMiddleware())
    dispatcher.include_router(notify_service_router)
