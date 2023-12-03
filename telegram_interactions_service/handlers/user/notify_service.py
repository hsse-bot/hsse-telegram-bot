from aiogram import F, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router
from telegram_interactions_service.states.notify_service_states import NotifySendTextForm
from telegram_interactions_service.misc import dataclasses, constants
from telegram_interactions_service.middlewares.admin_middleware import IsAdminMiddleware
from telegram_interactions_service.keyboards.inline import user

notify_service_router = Router()


@notify_service_router.message(Command("notify_service"))
async def cmd_notify_service(message: Message):
    await message.answer("Меню уведомлений", reply_markup=user.user_notify_service_menu_kb())


@notify_service_router.callback_query(user.NotifyCategoriesKb.filter(F.action == "/"))
async def call_categories_handler(callback: CallbackQuery, callback_data: user.NotifyCategoriesKb):
    categories = [dataclasses.NotifyCategory(id=i, name=f"Категория {i}") for i in range(constants.MAX_CATEGORIES_CNT)]
    await callback.message.edit_text(f"Категории уведомлений:",
                                     reply_markup=user.notify_categories_paginator_kb(categories, callback_data.page))
    await callback.answer()


@notify_service_router.callback_query(user.NotifyCategoriesKb.filter(F.action.in_(["/prev", "/next"])))
async def call_categories_pagination_handler(callback: CallbackQuery, callback_data: user.NotifyCategoriesKb):
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
            await callback.message.edit_text("Меню уведомлений",
                                             reply_markup=user.user_notify_service_menu_kb())
            await callback.answer()
            return
        next_categories_page = cur_page - 1
    await callback.message.edit_text(text="Категории уведомлений:",
                                     reply_markup=user.notify_categories_paginator_kb(categories, next_categories_page))
    await callback.answer()


@notify_service_router.callback_query(user.NotifyCategoriesKb.filter(F.action.startswith("/id/")))
async def call_category_handler(callback: CallbackQuery, callback_data: user.NotifyCategoriesKb):
    category_id = int(callback_data.action[4:])
    await callback.message.edit_text(f"Категория номер {category_id}",
                                     reply_markup=user.user_notify_category_kb(category_id, callback_data.page))
    await callback.answer()


@notify_service_router.callback_query(user.NotifyCategoryKb.filter(F.action.endswith("/unsubscribe")))
async def call_delete_category_handler(callback: CallbackQuery, callback_data: user.NotifyCategoryKb):
    category_id = callback_data.category_id
    # request to api to unsubscribe user from ategory
    await callback.message.edit_text(f"Вы успешно отписались от ведомлений категории {category_id}",
                                     reply_markup=user.user_return_notify_categories_kb())
    await callback.answer()


def setup(*, dispatcher: Dispatcher):
    notify_service_router.message.middleware(IsAdminMiddleware())
    dispatcher.include_router(notify_service_router)
