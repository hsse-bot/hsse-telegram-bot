from typing import Any, Awaitable, Callable, Dict, NoReturn

from aiogram import BaseMiddleware
from aiogram.types import Message

from ..config import SUPER_ADMIN_TG_ID


class IsSuperAdminMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message, data: Dict[str, Any]) -> Any:
        user_tg_id = event.from_user.id
        if user_tg_id == SUPER_ADMIN_TG_ID:
            return await handler(event, data)
