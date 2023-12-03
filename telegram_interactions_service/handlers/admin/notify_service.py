from aiogram import F, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router
from telegram_interactions_service.states.notify_service_states import NotifySendTextForm
from telegram_interactions_service.misc import dataclasses, constants
from telegram_interactions_service.middlewares.admin_middleware import IsAdminMiddleware
from telegram_interactions_service.keyboards.inline import admin

notify_service_router = Router()


@notify_service_router.message(Command("notify_service"))
async def cmd_notify_service(message: Message):
    await message.answer("Меню сервиса уведомлений", reply_markup=admin.admin_notify_service_menu_kb)


@notify_service_router.callback_query(admin.NotifyCategoriesKb.filter(F.action == "/"))
async def call_categories_handler(callback: CallbackQuery, callback_data: admin.NotifyCategoriesKb):
    categories = [dataclasses.NotifyCategory(id=i, name=f"Категория {i}") for i in range(constants.MAX_CATEGORIES_CNT)]
    await callback.message.edit_text(f"Категории уведомлений:",
                                     reply_markup=admin.notify_categories_paginator(categories, callback_data.page))
    await callback.answer()


@notify_service_router.callback_query(admin.NotifyCategoriesKb.filter(F.action.in_(["/prev", "/next"])))
async def call_categories_pagination_handler(callback: CallbackQuery, callback_data: admin.NotifyCategoriesKb):
    # categories = get_all_categories()
    categories = [dataclasses.NotifyCategory(id=i, name=f"Категория {i}") for i in range(constants.MAX_CATEGORIES_CNT)]
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
                                             reply_markup=admin.admin_notify_service_menu_kb)
            await callback.answer()
            return
        next_categories_page = cur_page - 1
    await callback.message.edit_text(text="Категории уведомлений:",
                                     reply_markup=admin.notify_categories_paginator(categories, next_categories_page))
    await callback.answer()


@notify_service_router.callback_query(admin.NotifyCategoriesKb.filter(F.action.startswith("/id/")))
async def call_category_handler(callback: CallbackQuery, callback_data: admin.NotifyCategoriesKb):
    category_id = int(callback_data.action[4:])
    await callback.message.edit_text(f"Категория номер {category_id}",
                                     reply_markup=admin.admin_notify_category(category_id, callback_data.page))
    await callback.answer()


@notify_service_router.callback_query(admin.NotifyCategoryKb.filter(F.action.endswith("/send_text")))
async def call_send_text_handler(callback: CallbackQuery, callback_data: admin.NotifyCategoryKb, state: FSMContext):
    category_id = callback_data.category_id
    await state.set_state(NotifySendTextForm.text)
    await state.update_data(category_id=category_id)
    await callback.message.edit_text("Введите текст сообщения:")
    await callback.answer()


@notify_service_router.callback_query(admin.NotifyCategoryKb.filter(F.action.endswith("/delete")))
async def call_delete_category_handler(callback: CallbackQuery, callback_data: admin.NotifyCategoryKb):
    category_id = callback_data.category_id
    # request to api to delete category
    await callback.message.edit_text(f"Вы успешно удалили категорию {category_id}",
                                     reply_markup=admin.admin_return_menu_kb)
    await callback.answer()


@notify_service_router.message(NotifySendTextForm.text)
async def receive_notify_message_text(message: Message, state: FSMContext):
    category_id = (await state.get_data())["category_id"]
    # request to api to send message.text
    await state.clear()
    await message.answer(f"Вы успешно отправили текст {message.text}", reply_markup=admin.admin_return_menu_kb)


def setup(*, dispatcher: Dispatcher):
    notify_service_router.message.middleware(IsAdminMiddleware())
    dispatcher.include_router(notify_service_router)
