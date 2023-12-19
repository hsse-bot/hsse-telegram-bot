import logging

from aiogram import F, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router

from telegram_interactions_service.misc import dataclasses, constants
from telegram_interactions_service.middlewares import IsRegisteredMiddleware
from telegram_interactions_service.keyboards.inline import user
from telegram_interactions_service.services_interactions.telegram_notifier_service import \
    TelegramNotifierServiceInteraction
from telegram_interactions_service.exceptions import TelegramNotifierServiceError
from telegram_interactions_service.misc import message_templates

notify_service_router = Router()
logger = logging.getLogger(__name__)


@notify_service_router.message(Command("notify_service"))
async def cmd_notify_service(message: Message):
    await message.answer("Меню уведомлений", reply_markup=user.user_notify_service_menu_kb())


@notify_service_router.callback_query(user.NotifyCategoriesKb.filter(F.action == "/"))
async def call_categories_handler(callback: CallbackQuery, callback_data: user.NotifyCategoriesKb):
    try:
        all_categories = await TelegramNotifierServiceInteraction().get_all_categories()
        user_categories = await TelegramNotifierServiceInteraction().get_user_categories(callback.from_user.id)
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await callback.message.edit_text(message_templates.error_user_text, reply_markup=user.error_kb())
        await callback.answer()
        return
    if len(all_categories) == 0:
        await callback.message.edit_text(f"Пока что нет категорий уведомлений",
                                         reply_markup=user.error_kb())
        await callback.answer()
        return
    max_page, cur_page = (len(all_categories) - 1) // constants.MAX_CATEGORIES_PER_PAGE, int(callback_data.page)
    await callback.message.edit_text(f"Категории уведомлений: {cur_page+1}/{max_page+1}",
                                     reply_markup=user.notify_categories_paginator_kb(all_categories,
                                                                                      user_categories,
                                                                                      callback_data.page))
    await callback.answer()


@notify_service_router.callback_query(user.NotifyCategoriesKb.filter(F.action.in_(["/prev", "/next"])))
async def call_categories_pagination_handler(callback: CallbackQuery, callback_data: user.NotifyCategoriesKb):
    try:
        all_categories = await TelegramNotifierServiceInteraction().get_all_categories()
        user_categories = await TelegramNotifierServiceInteraction().get_user_categories(callback.from_user.id)
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await callback.message.edit_text(message_templates.error_user_text, reply_markup=user.error_kb())
        await callback.answer()
        return
    if len(all_categories) == 0:
        await callback.message.edit_text(f"Пока что нет категорий уведомлений",
                                         reply_markup=user.error_kb())
        await callback.answer()
        return
    max_page, cur_page = (len(all_categories) - 1) // constants.MAX_CATEGORIES_PER_PAGE, int(callback_data.page)
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
    await callback.message.edit_text(text=f"Категории уведомлений: {next_categories_page+1}/{max_page+1}",
                                     reply_markup=user.notify_categories_paginator_kb(all_categories, user_categories, next_categories_page))
    await callback.answer()


@notify_service_router.callback_query(user.NotifyCategoriesKb.filter(F.action.startswith("/id/")))
async def call_category_handler(callback: CallbackQuery, callback_data: user.NotifyCategoriesKb):
    if callback_data.action.startswith("/id/sub/"):
        category_id = int(callback_data.action[8:])
        try:
            await TelegramNotifierServiceInteraction().sub_user_to_category(callback.from_user.id, category_id)
            category = await TelegramNotifierServiceInteraction().get_category(category_id)
        except Exception as error:
            logger.log(level=logging.ERROR, msg=error, exc_info=True)
            await callback.message.edit_text(message_templates.error_fail_to_sub_category_text,
                                             reply_markup=user.error_kb())
            await callback.answer()
            return
        await call_categories_pagination_handler(callback, callback_data)
        return
        # await callback.message.edit_text(f"Вы успешно подписались на уведомления {category.name}",
        #                                  reply_markup=user.user_return_notify_categories_kb())
        # await callback.answer()
    elif callback_data.action.startswith("/id/unsub/"):
        category_id = int(callback_data.action[10:])
        try:
            await TelegramNotifierServiceInteraction().unsub_user_to_category(callback.from_user.id, category_id)
            category = await TelegramNotifierServiceInteraction().get_category(category_id)
        except Exception as error:
            logger.log(level=logging.ERROR, msg=error, exc_info=True)
            await callback.message.edit_text(message_templates.error_fail_to_unsub_category_text,
                                             reply_markup=user.error_kb())
            await callback.answer()
            return
        await call_categories_pagination_handler(callback, callback_data)
        # return
        # await callback.message.edit_text(f"Вы успешно отписались от уведомлений категории {category.name}",
        #                                  reply_markup=user.user_return_notify_categories_kb())
        # await callback.answer()
    else:
        logger.log(level=logging.ERROR, msg=f"unknown action '{callback_data.action}'")


def setup(*, dispatcher: Dispatcher):
    notify_service_router.message.middleware(IsRegisteredMiddleware())
    dispatcher.include_router(notify_service_router)
