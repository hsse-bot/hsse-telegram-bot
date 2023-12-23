from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from ..config import SUPER_ADMIN_TG_ID
from telegram_interactions_service.services_interactions.user_managing_service import UserManagingServiceInteraction


class IsAdminMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message, data: Dict[str, Any]) -> Any:
        user_tg_id = event.from_user.id
        user_managing_service = UserManagingServiceInteraction()
        if await user_managing_service.is_admin(user_tg_id) or user_tg_id == SUPER_ADMIN_TG_ID:
            return await handler(event, data)
