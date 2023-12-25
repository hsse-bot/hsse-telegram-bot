import logging

from aiogram import F, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router

from telegram_interactions_service.misc import dataclasses, constants
from telegram_interactions_service.middlewares import IsRegisteredMiddleware
from telegram_interactions_service.keyboards.inline import user
from telegram_interactions_service.services_interactions.user_managing_service import \
    UserManagingServiceInteraction
from telegram_interactions_service.exceptions import TelegramNotifierServiceError
from telegram_interactions_service.misc import message_templates

rating_router = Router()
logger = logging.getLogger(__name__)


@rating_router.callback_query(user.UserMainMenuKb.filter(F.action == "/rating"))
async def rating_handler(callback: CallbackQuery, callback_data: user.RatingMenuKb):
    try:
        top_users = await UserManagingServiceInteraction().get_top_scores()
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await callback.message.edit_text(message_templates.error_user_text, reply_markup=user.error_kb())
        await callback.answer()
        return
    text = ''
    for number, user_in_top in enumerate(top_users):
        text += f'{number + 1}. {user_in_top.surname} {user_in_top.name} - {user_in_top.score}\n'
    await callback.message.edit_text('Рейтинг студентов\nЗарабатывай очки, выполняя поручения студсовета\n\n'
                                     'Топ:\n' + text, reply_markup=user.rating_kb())


def setup(*, dispatcher: Dispatcher):
    rating_router.message.middleware(IsRegisteredMiddleware())
    dispatcher.include_router(rating_router)
