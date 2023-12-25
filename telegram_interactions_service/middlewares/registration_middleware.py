import logging
from typing import Any, Awaitable, Callable, Dict, NoReturn

from aiogram import BaseMiddleware
from aiogram.types import Message

from telegram_interactions_service.services_interactions.user_managing_service import UserManagingServiceInteraction
from telegram_interactions_service.misc.message_templates import error_in_middleware


logger = logging.getLogger(__name__)


class IsUnregisteredMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message, data: Dict[str, Any]) -> Any:
        user_tg_id = event.from_user.id
        try:
            user_managing_service = UserManagingServiceInteraction()
            is_banned = await user_managing_service.is_banned(user_tg_id)
            if is_banned:
                return
            if await user_managing_service.get_user(user_tg_id) is None:
                return await handler(event, data)
        except Exception as error:
            logger.log(level=logging.ERROR, msg=error, exc_info=True)
            await event.answer(error_in_middleware)


class IsRegisteredMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message, data: Dict[str, Any]) -> Any:
        user_tg_id = event.from_user.id
        try:
            user_managing_service = UserManagingServiceInteraction()
            is_banned = await user_managing_service.is_banned(user_tg_id)
            if is_banned:
                return
            if await user_managing_service.get_user(user_tg_id) is not None:
                return await handler(event, data)
            await event.answer("Зарегистрируйтесь! /reg")
        except Exception as error:
            logger.log(level=logging.ERROR, msg=error, exc_info=True)
            await event.answer(error_in_middleware)