from aiogram import Dispatcher
from aiohttp.web_app import Application
from telegram_interactions_service.handlers import user, admin, super_admin, web, hooks
from typing import NoReturn


def setup(*, dispatcher: Dispatcher, web_app: Application) -> NoReturn:
    super_admin.setup(dispatcher=dispatcher)
    admin.setup(dispatcher=dispatcher)
    user.setup(dispatcher=dispatcher)
    hooks.setup(dispatcher=dispatcher)
    web.setup(web_app=web_app)


__all__ = ["setup"]
