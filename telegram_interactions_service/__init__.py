from aiohttp import web
from telegram_interactions_service import config
from urllib.parse import urlparse
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.fsm.strategy import FSMStrategy
from aiogram.webhook.aiohttp_server import TokenBasedRequestHandler, setup_application

from telegram_interactions_service import handlers
from typing import NoReturn
from aioredis import Redis


def start() -> NoReturn:
    bot = Bot(token=config.TOKEN_API, parse_mode=ParseMode.HTML)

    storage = RedisStorage(
        redis=Redis(host=config.REDIS_HOST, port=config.REDIS_PORT),
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True)
    )

    dispatcher = Dispatcher(
        storage=storage,
        fsm_strategy=FSMStrategy.USER_IN_CHAT,
    )

    web_app = web.Application()
    # middlewares.setup(dispatcher=dispatcher, i18n=i18n)
    handlers.setup(dispatcher=dispatcher, web_app=web_app)

    webhook_url_info = urlparse(config.WEBHOOK_URL)
    web_handler = TokenBasedRequestHandler(dispatcher=dispatcher)
    web_handler.register(web_app, path=webhook_url_info.path)
    setup_application(web_app, dispatcher, bot=bot)
    web.run_app(app=web_app, host=config.WEB_APP_HOST, port=config.WEB_SERVER_PORT)


__all__ = ["start"]
