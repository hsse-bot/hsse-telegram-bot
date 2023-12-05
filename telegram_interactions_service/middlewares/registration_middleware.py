from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Any, Awaitable, Callable, Dict, NoReturn
from telegram_interactions_service.services_interactions.user_managing_service import UserManagingServiceInteraction


class IsUnregisteredMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message, data: Dict[str, Any]) -> Any:
        user_tg_id = event.from_user.id
        user_managing_service = UserManagingServiceInteraction()
        if await user_managing_service.get_user(user_tg_id) is None:
            return await handler(event, data)
        await event.answer("Вы уже зарегистрированы!")


class IsRegisteredMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message, data: Dict[str, Any]) -> Any:
        user_tg_id = event.from_user.id
        user_managing_service = UserManagingServiceInteraction()
        if await user_managing_service.get_user(user_tg_id) is not None:
            return await handler(event, data)
        await event.answer("Зарегистрируйтесь! /reg")
